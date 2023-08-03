import logging

from ValLib.debug import Level, env_setup

LOGGER_NAME = "ValChange"

logger = logging.getLogger(LOGGER_NAME)

env_setup(logger)

childs = {
    "riot": logger.getChild("riot"),
    "locale": logger.getChild("locale"),
}


def log(level: int, msg: object, child="default"):
    if child in childs:
        childs[child].log(level, msg)
        return
    logger.log(level, msg)


__all__ = ["log", "Level"]
