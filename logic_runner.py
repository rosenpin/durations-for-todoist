from db.db import DB
from duration_setter import DurationSetter
from logic import Logic
from modes.labels import LabelsMode
from modes.projects import ProjectsMode
from todoist_wrapper.todoist_api_wrapper import TodoistAPIWrapper

modes = {
    "projects": ProjectsMode,
    "labels": LabelsMode
}

db = DB()


def run_specific_task_for_user(user_id, task_id):
    user = db.get_user_by_user_id(user_id=user_id)

    doist = TodoistAPIWrapper(token=user.token)
    duration_setter = DurationSetter(doist)

    logic = Logic(ds=duration_setter, doist=doist)
    logic.run_specific_task(mode=modes[user.mode](doist=doist), task_id=task_id)


def run_for_user(user_id):
    user = db.get_user_by_user_id(user_id=user_id)

    doist = TodoistAPIWrapper(token=user.token)
    duration_setter = DurationSetter(doist)

    logic = Logic(ds=duration_setter, doist=doist)
    logic.run(modes[user.mode](doist=doist))


def run_for_all_users():
    users = db.get_all_users()

    for user in users:
        run_for_user(user.user_id)
