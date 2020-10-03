from todoist.models import Item

from duration_setter import DurationSetter
from modes.mode import Mode
from todoist_wrapper.todoist_wrapper import TodoistWrapper


class Logic:
    def __init__(self, ds: DurationSetter):
        self.ds = ds

    def handle_task(self, task: Item, mode: Mode):
        duration = mode.get_duration(task)
        self.ds.set_duration(task=task, duration=duration)

    def run(self, mode: Mode):
        mode.prepare()

        tasks = mode.get_relevant_tasks()
        for task in tasks:
            self.handle_task(task=task, mode=mode)
