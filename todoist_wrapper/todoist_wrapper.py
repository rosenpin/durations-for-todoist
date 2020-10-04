class TodoistWrapper:

    def get_all_labels(self):
        raise NotImplementedError()

    def get_tasks(self, filt):
        raise NotImplementedError

    def get_all_tasks(self):
        raise NotImplementedError()

    def get_task_by_id(self, item_id):
        raise NotImplementedError()

    def add_label(self, name):
        raise NotImplementedError()

    def get_label(self, label_id):
        raise NotImplementedError()

    def add_project(self, name):
        raise NotImplementedError()

    def sync(self):
        raise NotImplementedError()

    def commit(self):
        raise NotImplementedError()

    def get_project(self, project_id):
        raise NotImplementedError()

    def get_all_projects(self):
        raise NotImplementedError()

    def get_user_id(self):
        raise NotImplementedError()

    def get_user_name(self):
        raise NotImplementedError()
