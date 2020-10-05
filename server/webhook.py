import threading
import time

from flask import request, make_response

import logic_runner
from server.consts import *

ALL_TASKS_SUCCESS_MESSAGE = "SUCCESS you tasks won't be updated for the next 15 minutes"

HTTP_USER_ERROR = 401

USER_NOT_FOUND_MESSAGE = "user with user_id %s not found in db"

USER_IN_COOLDOWN_MESSAGE = "ignoring request because user is in cooldown"

instances = {}


def handle_all_user_tasks(user_id):
    if not should_handle_user(user_id=user_id):
        print(USER_IN_COOLDOWN_MESSAGE)
        return make_response(USER_IN_COOLDOWN_MESSAGE, HTTP_USER_ERROR)

    try:
        logic_runner.run_for_user(user_id=user_id)
        instances[user_id] = time.time() + 15 * MINUTE
        return make_response(ALL_TASKS_SUCCESS_MESSAGE)
    except KeyError:
        print(USER_NOT_FOUND_MESSAGE % user_id)
        return make_response(USER_NOT_FOUND_MESSAGE % user_id, HTTP_USER_ERROR)


def handle_user_task(user_id, task_id):
    try:
        logic_runner.run_specific_task_for_user(user_id=user_id, task_id=task_id)
        instances[user_id] = time.time()
    except KeyError:
        print(USER_NOT_FOUND_MESSAGE % user_id)


def should_handle_user(user_id):
    if user_id in instances:
        # if already busy updating tasks for this user
        # even after being busy we might still receive updates because we updated many tasks
        if instances[user_id] == BUSY_INSTANCE or instances[user_id] > time.time() - 30:
            return False
    return True


def handle_web_hook():
    req = request.json

    user_id = req[WEB_HOOK_USER_ID_FIELD]

    if not should_handle_user(user_id=user_id):
        print(USER_IN_COOLDOWN_MESSAGE)
        return

    task_id = req[WEB_HOOK_TASK_DATA][WEB_HOOK_TASK_ID]
    instances[user_id] = BUSY_INSTANCE

    thread = threading.Thread(target=handle_user_task, kwargs={
        'user_id': user_id,
        'task_id': task_id
    })
    thread.start()
