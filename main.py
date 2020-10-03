from db.db import DB
from duration_setter import DurationSetter
from logic import Logic
from modes.labels import LabelsMode
from modes.projects import ProjectsMode
from todoist_wrapper.todoist_api_wrapper import TodoistAPIWrapper

modes = {
    "projects": ProjectsMode,
    "labels": LabelsMode
}


def main():
    db = DB()
    users = db.get_all_users()

    for user in users:
        doist = TodoistAPIWrapper(token=user.token)

        duration_setter = DurationSetter(doist)

        logic = Logic(ds=duration_setter)
        logic.run(modes[user.mode](doist=doist))


if __name__ == '__main__':
    main()
