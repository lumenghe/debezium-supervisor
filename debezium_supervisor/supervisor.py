import logging
import os
import time

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class Supervisor:
    def __init__(self, kafka_config, cdc_config):
        self._kafka_config = kafka_config
        self._logger = logger
        self._url = f"""https://{cdc_config}:8443/connectors"""
        self._verify = self._kafka_config["extra_params"]["ssl.ca.location"]
        self._cert = (
            self._kafka_config["extra_params"]["ssl.certificate.location"],
            self._kafka_config["extra_params"]["ssl.key.location"],
        )
