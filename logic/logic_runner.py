import logging

from todoist_service.db import DB
from todoist_service.todoist_wrapper.todoist_api_wrapper import TodoistAPIWrapper

from consts import consts
from duration_setter.duration_setter import DurationSetter
from logic.logic import Logic
from modes.labels import LabelsMode
from modes.projects import ProjectsMode

modes = {
    "projects": ProjectsMode,
    "labels": LabelsMode
}


def create_logic(db, user_id):
    logging.debug("creating logic for user id {user_id}".format(user_id=user_id))
    user = db.get_user_by_user_id(user_id=user_id)
    logging.debug("user is {user}".format(user=user))

    doist = TodoistAPIWrapper(token=user.token)
    duration_setter = DurationSetter(doist)

    logging.debug("user mode is {user_mode}".format(user_mode=user.mode))
    logic = Logic(ds=duration_setter, doist=doist, mode=modes[user.mode](doist=doist))
    return logic


def run_specific_task_for_user(db, user_id, task_id):
    logic = create_logic(db=db, user_id=user_id)
    logic.run_specific_task(task_id=task_id)


def run_for_user(db, user_id):
    logic = create_logic(db=db, user_id=user_id)
    logic.run()


def run_for_all_users():
    db = DB.get_instance(consts.db_path)

    users = db.get_all_users()

    for user in users:
        run_for_user(db=db, user_id=user.user_id)
