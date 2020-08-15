import logging
import logging.config
import os
import traceback

import click
import yaml

from debezium_supervisor.supervisor import Supervisor

logger = logging.getLogger(__name__)


@click.command()
def main():
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)
    try:

        # handle config log
        logging.config.dictConfig(cfg["log"])

        supervisor = Supervisor(
            kafka_config=cfg["kafka"], cdc_config=cfg["cdc"]
        )
        supervisor.start()
    # reason: we want to catch all exceptions
    except Exception as e:
        stacktrace = traceback.format_exc()
        logger.error("{}: {}".format(e.__class__.__name__, stacktrace))