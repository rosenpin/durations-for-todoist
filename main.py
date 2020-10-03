from duration_setter import DurationSetter
from logic import Logic
from modes.projects import ProjectsMode
from todoist_wrapper.todoist_api_wrapper import TodoistAPIWrapper


def main():
    doist = TodoistAPIWrapper(token="62ef7a3d01db63f92ca821e6f04674987aa3a3e6")

    duration_setter = DurationSetter(doist)

    logic = Logic(ds=duration_setter)
    logic.run(ProjectsMode(doist=doist))


if __name__ == '__main__':
    main()
