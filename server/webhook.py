import logging
import threading
import time

from flask import request, make_response

import logic_runner
import utils
from server.consts import *

instances = {}


def handle_all_user_tasks(db, user_id):
    if not should_handle_user(user_id=user_id):
        logging.info(USER_IN_COOLDOWN_MESSAGE)
        return make_response(USER_IN_COOLDOWN_MESSAGE, HTTP_USER_ERROR)

    try:
        logic_runner.run_for_user(db=db, user_id=user_id)
        instances[cooldown_key(user_id, "")] = time.time() + UPDATE_ALL_COOLDOWN
        return make_response(ALL_TASKS_SUCCESS_MESSAGE)
    except KeyError as err:
        utils.log_error(err)
        return make_response(USER_NOT_FOUND_MESSAGE % user_id, HTTP_USER_ERROR)


def handle_user_task(db, user_id, task_id):
    try:
        logic_runner.run_specific_task_for_user(db=db, user_id=user_id, task_id=task_id)
        instances[cooldown_key(user_id, task_id)] = time.time()
    except KeyError as err:
        utils.log_error(err)
    except TypeError as err:
        # put in shorter cooldown if task is irrelevant
        instances[cooldown_key(user_id, task_id)] = time.time() - 20
        logging.info(err)


def should_handle_user(user_id, task_id=""):
    if cooldown_key(user_id, task_id) in instances:
        # if already busy updating tasks for this user
        # even after being busy we might still receive updates because we updated many tasks
        if int(instances[cooldown_key(user_id, task_id)]) == BUSY_INSTANCE or \
                int(instances[cooldown_key(user_id, task_id)]) > time.time() - 30:
            logging.debug("shouldn't handle user")
            return False

    # also check if user might be in cooldown
    if task_id != "":
        return should_handle_user(user_id=user_id, task_id="")
    return True


def handle_web_hook(db):
    req = request.json

    user_id = req[WEB_HOOK_USER_ID_FIELD]
    task_id = req[WEB_HOOK_TASK_DATA][WEB_HOOK_TASK_ID]

    if not should_handle_user(user_id=user_id, task_id=task_id):
        logging.info(USER_IN_COOLDOWN_MESSAGE)
        return

    instances[cooldown_key(user_id, task_id)] = BUSY_INSTANCE

    thread = threading.Thread(target=handle_user_task, kwargs={
        'db': db,
        'user_id': user_id,
        'task_id': task_id
    })
    thread.start()
