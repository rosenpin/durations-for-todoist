from todoist.models import Item

from duration_setter import DurationSetter
from modes.mode import Mode
from todoist_wrapper.todoist_wrapper import TodoistWrapper

TASK_ITEM_FIELD = "item"


class Logic:
    def __init__(self, ds: DurationSetter, doist: TodoistWrapper):
        self.ds = ds
        self.doist = doist

    def handle_task(self, task: Item, mode: Mode):
        duration = mode.get_duration(task)
        self.ds.set_duration(task=task, duration=duration)

    def run_specific_task(self, mode: Mode, task_id):
        mode.prepare()

        task = self.doist.get_task_by_id(task_id)
        if TASK_ITEM_FIELD not in task:
            print("invalid task provided to run_specific_task")
            print(task)
            return

        if mode.is_task_relevant(task=task[TASK_ITEM_FIELD]):
            self.handle_task(task=task[TASK_ITEM_FIELD], mode=mode)

    def run(self, mode: Mode):
        mode.prepare()

        tasks = mode.get_relevant_tasks()
        for task in tasks:
            self.handle_task(task=task, mode=mode)
