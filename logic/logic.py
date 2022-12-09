import logging
import sys

from todoist.models import Item
from todoist_api_python.models import Task
from todoist_service.todoist_wrapper.todoist_api_wrapper import TodoistAPIWrapper
from todoist_service.todoist_wrapper.todoist_wrapper import TodoistWrapper

from duration_setter.duration_setter import DurationSetter
from modes.labels import LabelsMode
from modes.mode import Mode

TASK_ITEM_FIELD = "item"


class Logic:
    def __init__(self, ds: DurationSetter, doist: TodoistWrapper, mode: Mode):
        self.ds = ds
        self.doist = doist
        self.mode = mode

    def handle_task(self, task: Task):
        duration = self.mode.get_duration(task=task)
        logging.info("task duration is {duration}".format(duration=duration))
        self.ds.set_duration(task=task, duration=duration)

    def run_specific_task(self, task_id):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        logging.info("running for specific task {task_id}".format(task_id=task_id))

        task = self.doist.get_task_by_id(task_id)

        if self.mode.is_task_relevant(task=task):
            logging.info("handling task")
            self.handle_task(task=task)
            return

        raise TypeError("task is not relevant {task}".format(task=task))

    def run(self):
        logging.info("running for all user tasks")

        tasks = self.mode.get_relevant_tasks()
        logging.info("got relevant tasks")

        for task in tasks:
            logging.info("handling task")
            self.handle_task(task=task)

        logging.info("handled all user tasks")