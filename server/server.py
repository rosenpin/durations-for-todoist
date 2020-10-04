import getpass
import os
import time
from threading import Thread

from flask import Flask, redirect, request, make_response
from oauthlib.oauth2 import WebApplicationClient

import logic_runner
from db.db import DB
from server.authorization import authorization
from server.consts import *
from server.settings import handle_settings


DEBUG = getpass.getuser() == "tomer"
if DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

client = WebApplicationClient(CLIENT_ID)

db = DB()

instances = {}


@app.route("/")
def index():
    user_id = request.cookies.get(COOKIE_USERID)
    if user_id:
        return redirect("settings")

    with open(HOME_PAGE, 'r') as file:
        data = file.read()
        return make_response(data)


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    req = request.json

    def handle_user_tasks(user_id):
        logic_runner.run_for_user(user_id)
        instances[user_id] = time.time()

    uid = req[WEB_HOOK_USER_ID_FIELD]

    # if already busy updating tasks for this user
    # even after being busy we might still receive updates because we updated many tasks
    if instances[uid] == BUSY_INSTANCE or instances[uid] > time.time() - 2 * MINUTE:
        return make_response("200 OK")

    instances[uid] = BUSY_INSTANCE
    thread = Thread(target=handle_user_tasks, kwargs={
        'user_id': uid
    })
    thread.start()

    return make_response("200 OK")


@app.route("/settings")
def settings():
    response = handle_settings(db=db)
    return response


@app.route("/submit")
def submit():
    mode = request.args.get("mode")
    user_id = request.cookies.get(COOKIE_USERID)
    db.update_user_mode(user_id=user_id, mode=mode)
    return redirect("settings")


@app.route('/authorize')
def authorize():
    response = authorization.handle_authorization_request(client=client)
    return response


@app.route("/redirect")
def redirect_url():
    response = authorization.handle_redirect_request(client=client)
    return response


def run_server():
    app.run(port=SERVER_PORT, debug=DEBUG)
