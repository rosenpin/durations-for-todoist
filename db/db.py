import json
import logging
from dataclasses import dataclass
from pathlib import Path

from tinydb import TinyDB, Query

DEFAULT_MODE = "undefined"

ACCESS_TOKEN = 'access_token'
FULL_NAME = "full_name"
USER_ID = 'user_id'
MODE = "mode"


@dataclass
class User:
    user_id: str
    user_name: str
    token: str
    mode: str

    def __init__(self, token, user_name, user_id, mode):
        self.token = token
        self.user_name = user_name
        self.user_id = user_id
        self.mode = mode

    @staticmethod
    def from_dict(user_dict):
        return User(token=user_dict[ACCESS_TOKEN],
                    user_name=user_dict[FULL_NAME],
                    user_id=user_dict[USER_ID],
                    mode=user_dict[MODE])


# SAMPLE_USER = User("1234", "dummy user", "1234", "labels")


class DB:
    __instance = None

    @staticmethod
    def get_instance():
        if DB.__instance is None:
            DB()
        return DB.__instance

    def __init__(self):
        logging.debug("creating DB object")
        if DB.__instance is not None:
            raise Exception("DB is a singleton")
        else:
            self.db = TinyDB(Path.home().joinpath("users.json"))
            DB.__instance = self

        # self.add_user(SAMPLE_USER.user_id, SAMPLE_USER.token, SAMPLE_USER.user_name, SAMPLE_USER.mode)

    def remove_user_by_token(self, token):
        self.db.remove(Query().access_token == token)

    def remove_user_by_user_id(self, user_id):
        self.db.remove(Query().user_id == user_id)

    def add_user(self, user_id, token, full_name, mode=DEFAULT_MODE):
        try:
            found = self.get_user_by_user_id(user_id=user_id)
            previous_mode = found.mode
            if mode == DEFAULT_MODE:
                mode = previous_mode
        except KeyError:
            pass

        self.remove_user_by_token(token=token)
        self.remove_user_by_user_id(user_id=user_id)
        self.db.insert({
            USER_ID: user_id,
            ACCESS_TOKEN: token,
            FULL_NAME: full_name,
            MODE: mode
        })

    def get_user_by_user_id(self, user_id: str) -> User:
        users = self.db.search(Query().user_id == str(user_id))
        if len(users) != 1:
            raise KeyError(f"Found {len(users)} users with user id {user_id}")

        return User.from_dict(users[0])

    def update_user_mode(self, user_id: str, mode: str):
        self.db.update({
            MODE: mode
        }, Query().user_id == user_id)

    def get_all_users(self):
        users = []
        for user in self.db.all():
            users.append(User.from_dict(user_dict=user))

        return users
