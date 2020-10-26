import abc

from todoist_service.todoist_wrapper.todoist_wrapper import TodoistWrapper


class Mode(metaclass=abc.ABCMeta):
    def __init__(self, doist: TodoistWrapper):
        self.doist = doist

    def prepare(self):
        raise NotImplementedError()

    def get_relevant_tasks(self):
        raise NotImplementedError()

    def get_duration(self, task) -> int:
        raise NotImplementedError()

    def is_task_relevant(self, task) -> bool:
        raise NotImplementedError()
