from todoist.models import Item

from duration_setter import DurationSetter
from modes.mode import Mode
from todoist_wrapper.todoist_wrapper import TodoistWrapper

TASK_ITEM_FIELD = "item"


class Logic:
    def __init__(self, ds: DurationSetter, doist: TodoistWrapper, mode: Mode):
        self.ds = ds
        self.doist = doist
        self.mode = mode

    def handle_task(self, task: Item):
        duration = self.mode.get_duration(task)
        self.ds.set_duration(task=task, duration=duration)

    def run_specific_task(self, task_id):
        self.mode.prepare()

        task = self.doist.get_task_by_id(task_id)
        if TASK_ITEM_FIELD not in task:
            print("invalid task provided to run_specific_task")
            print(task)
            return

        if self.mode.is_task_relevant(task=task[TASK_ITEM_FIELD]):
            self.handle_task(task=task[TASK_ITEM_FIELD])

    def run(self):
        self.mode.prepare()

        tasks = self.mode.get_relevant_tasks()
        for task in tasks:
            self.handle_task(task=task)
