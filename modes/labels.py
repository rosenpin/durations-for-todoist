from todoist.models import Item

import consts
from modes.mode import Mode
from todoist_wrapper.todoist_wrapper import TodoistWrapper


class LabelsMode(Mode):
    def __init__(self, doist: TodoistWrapper):
        super().__init__(doist)

    def prepare(self):
        labels = self.doist.get_all_labels()
        labels_names = list(map(lambda label: label[consts.LabelFields.Name], labels))

        for label_name in consts.duration_labels.keys():
            if label_name not in labels_names:
                self.doist.add_label(label_name)

    def get_relevant_tasks(self):
        return self.doist.get_tasks("@" + consts.clock_icon + "*")

    def get_duration(self, task: Item) -> int:
        task_labels = task[consts.TaskFields.Labels]
        for label in task_labels:
            if label in consts.duration_labels:
                return consts.duration_labels[label]
