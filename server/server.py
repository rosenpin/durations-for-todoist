import os

from flask import Flask, redirect, request, make_response
from oauthlib.oauth2 import WebApplicationClient

import logic_runner
from db.db import DB
from server.authorization import authorization
from server.consts import *
from server.settings import handle_settings

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)

client = WebApplicationClient(CLIENT_ID)

db = DB()


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    req = request.json
    user_id = req[WEB_HOOK_USER_ID_FIELD]
    logic_runner.run_for_user(user_id)
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
    app.run(port=SERVER_PORT)
