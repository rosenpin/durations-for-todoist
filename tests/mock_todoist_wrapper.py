from todoist_wrapper.todoist_wrapper import TodoistWrapper


class MockTodoistWrapper(TodoistWrapper):
    def get_all_labels(self):
        pass

    def get_all_tasks(self):
        pass

    def get_task_by_id(self, item_id):
        pass

    def add_label(self, name):
        pass

    def sync(self):
        pass

    def commit(self):
        pass
