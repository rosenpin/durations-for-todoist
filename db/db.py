from dataclasses import dataclass
from pathlib import Path

from tinydb import TinyDB, Query

ACCESS_TOKEN = 'access_token'
USER_ID = 'user_id'
MODE = "mode"


@dataclass
class User:
    user_id: str
    token: str
    mode: str

    def __init__(self, user_dict):
        self.token = user_dict[ACCESS_TOKEN]
        self.user_id = user_dict[USER_ID]
        self.mode = user_dict[MODE]


class DB:
    def __init__(self):
        self.db = TinyDB(Path.home().joinpath("users.json"))

    def remove_user_by_token(self, token):
        self.db.remove(Query().access_token == token)

    def remove_user_by_user_id(self, user_id):
        self.db.remove(Query().user_id == user_id)

    def add_user(self, user_id, token, mode="undefined"):
        self.remove_user_by_token(token=token)
        self.remove_user_by_user_id(user_id=user_id)
        self.db.insert({
            USER_ID: user_id,
            ACCESS_TOKEN: token,
            MODE: mode
        })

    def get_user_by_user_id(self, user_id: str) -> User:
        users = self.db.search(Query().user_id == user_id)
        if len(users) != 1:
            raise KeyError("User with user id %s not found" % user_id)
        return User(users[0])

    def update_user_mode(self, user_id: str, mode: str):
        self.db.update({
            MODE: mode
        }, Query().user_id == user_id)

    def get_all_users(self):
        users = []
        for user in self.db.all():
            users.append(User(user))

        return users