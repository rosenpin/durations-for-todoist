from todoist.models import Item

import consts
from consts import ProjectFields
from modes.mode import Mode
from todoist_wrapper.todoist_wrapper import TodoistWrapper


def is_duration_project(project_name):
    return project_name in consts.duration_labels


class ProjectsMode(Mode):
    def __init__(self, doist: TodoistWrapper):
        super().__init__(doist)

    def prepare(self):
        projects = self.doist.get_all_projects()
        project_names = list(map(lambda project: project[ProjectFields.Name], projects))

        for label in consts.duration_labels.keys():
            if label not in project_names:
                self.doist.add_project(label)

    def get_project_from_task(self, task):
        project_id = task[consts.TaskFields.ProjectID]
        project = self.doist.get_project(project_id=project_id)

        project_name = project[consts.ProjectFields.Project][consts.ProjectFields.Name]
        return project_name

    def get_relevant_tasks(self):
        return self.doist.get_tasks(lambda task: is_duration_project(project_name=self.get_project_from_task(task)))

    def get_duration(self, task: Item) -> int:
        project_name = self.get_project_from_task(task=task)
        if not is_duration_project(project_name=project_name):
            raise KeyError("Tried to get duration from task that is unmarked")

        return consts.duration_labels[project_name]
