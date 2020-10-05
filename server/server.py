import getpass
import os

from flask import Flask, redirect, request, make_response
from oauthlib.oauth2 import WebApplicationClient

from db.db import DB
from server.authorization import authorization
from server.consts import *
from server.settings import handle_settings, handle_submit
from server.webhook import handle_web_hook

DEBUG = getpass.getuser() == "tomer"
if DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

client = WebApplicationClient(CLIENT_ID)

db = DB()


@app.route("/")
def index():
    try:
        user_id = request.cookies.get(COOKIE_USERID)
        if user_id:
            return redirect("settings")

        with open(HOME_PAGE, 'r') as file:
            data = file.read()
            return make_response(data)
    except Exception as err:
        return make_response(SERVER_ERROR_MESSAGE.format(error=err))


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        handle_web_hook()
    except Exception as err:
        print(WEBHOOK_ERROR_MESSAGE.format(request=request.json, error=err))

    return make_response("200 OK")


@app.route("/settings")
def settings():
    try:
        response = handle_settings(db=db)
        return response
    except Exception as e:
        return make_response(SERVER_ERROR_MESSAGE.format(error=e), 501)


@app.route("/submit")
def submit():
    try:
        response = handle_submit(db=db)
        return response
    except Exception as err:
        return SERVER_ERROR_MESSAGE.format(error=err)


@app.route('/authorize')
def authorize():
    try:
        response = authorization.handle_authorization_request(client=client)
        return response
    except Exception as err:
        return SERVER_ERROR_MESSAGE.format(error=err)


@app.route("/redirect")
def redirect_url():
    try:
        response = authorization.handle_redirect_request(client=client)
        return response
    except Exception as err:
        return SERVER_ERROR_MESSAGE.format(error=err)


def run_server():
    app.run(port=SERVER_PORT, debug=DEBUG)
