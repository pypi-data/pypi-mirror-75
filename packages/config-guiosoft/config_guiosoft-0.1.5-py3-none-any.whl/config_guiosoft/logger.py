import logging

LOG = None


def get_logger() -> logging.Logger:
    global LOG
    if not LOG:
        LOG = logging.getLogger('config_guiosoft')
    return LOG
