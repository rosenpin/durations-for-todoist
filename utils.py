import logging
import traceback


def log_error(err):
    logging.error(err)
    logging.error(traceback.format_exc())