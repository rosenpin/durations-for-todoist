import random
import string

from flask import redirect, request, abort, make_response, url_for
from requests_oauthlib import OAuth2Session

from server.consts import *
from .registration import register_user


def handle_authorization_request(client):
    generated_state = ''.join(
        random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(random.randint(80, 100)))

    result = client.prepare_request_uri(TODOIST_AUTHORIZE_URL,
                                        redirect_uri=SERVER_REDIRECT_URL,
                                        scope=TODOIST_PREMISSIONS, state=generated_state)

    response = redirect(result)
    response.set_cookie(COOKIE_STATE, generated_state)
    return response




def handle_redirect_request(client):
    # validate state
    expected_state = request.cookies.get(COOKIE_STATE)
    if not expected_state == request.args.get(PARAM_STATE):
        abort(make_response("invalid state"))

    # parse uri params
    url = request.url.replace(INNER_SERVER, OUTER_SERVER)
    parsed = client.parse_request_uri_response(url, state=expected_state)

    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=TODOIST_TOKEN_URL,
                              client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET,
                              include_client_id=True,
                              code=parsed[PARAM_CODE])

    # register user to system
    token, user_id = register_user(access_token=token[PARAM_ACCESS_TOKEN])

    # redirect user to the settings page
    response = redirect(url_for(".settings"))

    # set the cookie so that we can recognize the user
    response.set_cookie(COOKIE_USERID, user_id)

    return response
