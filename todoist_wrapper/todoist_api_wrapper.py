import logging

from todoist import TodoistAPI

import consts
from todoist_wrapper.todoist_wrapper import TodoistWrapper


class TodoistAPIWrapper(TodoistWrapper):
    def __init__(self, token):
        self.api = TodoistAPI(token=token)
        self.api.reset_state()
        self.sync()

    def get_user_id(self):
        return self.api.user.get_id()

    def get_user_name(self):
        return self.api.user.state[consts.STATE_USER_FIELD][consts.STATE_USER_FULL_NAME_FIELD]

    def get_all_labels(self):
        return self.api.labels.all()

    def get_tasks(self, filt):
        return self.api.items.all(filt=filt)

    def get_all_tasks(self):
        return self.api.items.all()

    def get_task_by_id(self, item_id):
        return self.api.items.get_by_id(item_id)

    def add_label(self, name):
        self.api.labels.add(name=name)
        self.commit()

    def get_label(self, label_id):
        return self.api.labels.get(label_id=label_id)

    def add_project(self, name):
        self.api.projects.add(name=name)
        self.commit()

    def get_project(self, project_id):
        return self.api.projects.get(project_id=project_id)

    def get_all_projects(self):
        return self.api.projects.all()

    def sync(self):
        return self.api.sync()

    def commit(self):
        logging.debug(f"queue is {self.api.queue}")
        return self.api.commit()
