from todoist_api_python.models import Task
from todoist_service.todoist_wrapper.todoist_wrapper import TodoistWrapper

from consts import consts as duration_consts
from modes.mode import Mode


class LabelsMode(Mode):
    def __init__(self, doist: TodoistWrapper):
        super().__init__(doist)

    def prepare(self):
        labels = self.doist.get_all_labels()
        labels_names = list(map(lambda label: label.name, labels))

        for label_name in duration_consts.duration_labels.keys():
            if label_name not in labels_names:
                self.doist.add_label(label_name)

    def is_task_relevant(self, task) -> bool:
        return self.is_duration_label_available(task=task)

    def get_relevant_tasks(self):
        return self.doist.get_tasks(lambda task: self.is_task_relevant(task=task))

    def get_label_name_from_id(self, label_id):
        print("getting label for label id %s" % label_id)
        label = self.doist.get_label(label_id=label_id)

        label_name = label.name
        return label_name

    def get_duration(self, task: Task) -> int:
        task_labels_names = task.labels
        for label_name in task_labels_names:
            if label_name in duration_consts.duration_labels:
                return duration_consts.duration_labels[label_name]

        return 0

    def is_duration_label_available(self, task):
        return self.get_duration(task) != 0
