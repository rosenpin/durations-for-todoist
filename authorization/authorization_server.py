import os
import random
import string

from flask import Flask, redirect, request, abort, make_response, url_for
from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib import OAuth2Session

from authorization import registration
from db.db import DB
from .consts import *

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)

client = WebApplicationClient(CLIENT_ID)

db = DB()


@app.route("/settings")
def settings():
    user_id = request.cookies.get(USER_ID_COOKIE_NAME)
    user = db.get_user_by_user_id(user_id=user_id)
    with open(HOME_PAGE, 'r') as file:
        data = file.read() \
            .replace(CURRENT_MODE_PH, user.mode) \
            .replace(CURRENT_USER_PH, user.user_id)
        for mode in modes:
            if mode == user.mode:
                data = data.replace(MODE_FORMAT.format(mode=mode), HTML_CHECKED)
            else:
                data = data.replace(MODE_FORMAT.format(mode=mode), "")

        return make_response(data)


@app.route("/submit")
def submit():
    mode = request.args.get("mode")
    user_id = request.cookies.get(USER_ID_COOKIE_NAME)
    db.update_user_mode(user_id=user_id, mode=mode)
    return redirect("settings")


@app.route('/authorize')
def authorize():
    generated_state = ''.join(
        random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(random.randint(80, 100)))

    result = client.prepare_request_uri("https://todoist.com/oauth/authorize",
                                        redirect_uri="https://durations.rosenpin.io/redirect",
                                        scope="data:read_write", state=generated_state)

    response = redirect(result)
    response.set_cookie("state", generated_state)
    return response


@app.route("/redirect")
def redirect_url():
    expected_state = request.cookies.get("state")
    if not expected_state == request.args.get("state"):
        abort(make_response("invalid state"))

    parsed = client.parse_request_uri_response(request.url, state=expected_state)

    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url='https://todoist.com/oauth/access_token',
                              client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET,
                              include_client_id=True,
                              code=parsed["code"])
    token, user_id = registration.register_user(access_token=token["access_token"])
    response = redirect(url_for(".settings"))
    response.set_cookie(USER_ID_COOKIE_NAME, user_id)
    return response


if __name__ == '__main__':
    app.run()
