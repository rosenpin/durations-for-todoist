import logging
import re

from consts import TaskFields
from todoist_wrapper.todoist_wrapper import TodoistWrapper

DURATION_FORMAT = "{original} [{duration}m]"
DURATION_PATTERN = ".* \[\d+m\]$"


class DurationSetter:
    def __init__(self, doist: TodoistWrapper):
        self.doist = doist
        self.regex = re.compile(DURATION_PATTERN)

    def set_duration(self, task, duration):
        title = task[TaskFields.Title]
        if self.already_annotated(title=title):
            logging.info("skipping %s. already annotated" % title)
            return

        logging.info("set {title} duration to {duration}".format(title=title, duration=duration))
        new_title = DURATION_FORMAT.format(original=title, duration=duration)
        logging.debug(f"task new title is {new_title}")
        task.update(content=new_title)
        self.doist.commit()

    def already_annotated(self, title) -> bool:
        return self.regex.match(title) is not None
