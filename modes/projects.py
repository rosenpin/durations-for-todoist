import logging

from todoist.models import Item
from todoist_service import consts

from todoist_service.consts import ProjectFields

from consts import consts as durations_consts
from modes.mode import Mode
from todoist_service.todoist_wrapper.todoist_wrapper import TodoistWrapper


class ProjectsMode(Mode):
    def __init__(self, doist: TodoistWrapper):
        super().__init__(doist)

    def prepare(self):
        logging.debug("preparing projects mode")
        projects = self.doist.get_all_projects()
        project_names = list(map(lambda project: project[ProjectFields.Name], projects))

        for label in durations_consts.duration_labels.keys():
            if label not in project_names:
                self.doist.add_project(label)

        logging.debug("prepared projects mode successfully")

    def is_task_relevant(self, task) -> bool:
        return self.get_duration(task=task) != 0

    def get_relevant_tasks(self):
        return self.doist.get_tasks(lambda task: self.is_task_relevant(task=task))

    def get_duration(self, task: Item) -> int:
        logging.debug("getting task duration")
        project_name = self.get_project_from_task(task=task)
        if project_name in durations_consts.duration_labels:
            return durations_consts.duration_labels[project_name]

        logging.debug("couldn't get task duration")
        return 0

    def get_project_from_task(self, task):
        logging.debug("getting project from task")
        project_id = task[consts.TaskFields.ProjectID]
        project = self.doist.get_project(project_id=project_id)

        project_name = project[consts.ProjectFields.Project][consts.ProjectFields.Name]
        logging.debug("project name: {project_name}".format(project_name=project_name))

        return project_name
