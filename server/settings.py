import logging

from flask import request, make_response, redirect

from .consts import *


def add_mode(page, user):
    return page.replace(HTML_CURRENT_MODE_PH, user.mode)


def add_user_name(page, user):
    return page.replace(HTML_CURRENT_USER_PH, user.user_name)


def mark_selected_mode(page, user):
    for mode in modes:
        if mode == user.mode:
            page = page.replace(HTML_MODE_FORMAT.format(mode=mode), HTML_CHECKED)
            continue

        page = page.replace(HTML_MODE_FORMAT.format(mode=mode), "")

    return page


def handle_settings(db):
    user_id = request.cookies.get(COOKIE_USERID)
    if not user_id:
        return redirect("/")

    try:
        user = db.get_user_by_user_id(user_id=user_id)
    except KeyError as err:
        logging.error(err)
        response = redirect("/")
        response.delete_cookie(COOKIE_USERID)
        return response

    with open(SETTINGS_PAGE, 'r') as file:
        data = file.read()

        data = add_mode(data, user)
        data = add_user_name(data, user)
        data = mark_selected_mode(data, user)

        return make_response(data)


def handle_submit(db):
    mode = request.args.get("mode")
    user_id = request.cookies.get(COOKIE_USERID)
    db.update_user_mode(user_id=user_id, mode=mode)
    mode.prepare()
    return redirect(SETTINGS_PAGE_LOCATION)
