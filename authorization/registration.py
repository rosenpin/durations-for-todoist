from db.db import DB
from todoist_wrapper.todoist_api_wrapper import TodoistAPIWrapper


def register_user(access_token: str):
    doist = TodoistAPIWrapper(access_token)
    user_id = str(doist.get_user_id())
    db = DB()
    db.add_user(user_id=user_id, token=access_token)
    return access_token, user_id
