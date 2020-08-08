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

    def start(self):
        while True:
            try:
                time.sleep(0.5)
                connectors = self.get_connectors()
                response = self.get_status(max(connectors))
                self.send_state_metrics(response)
                self._logger.info("api_status: ok")
            except requests.exceptions.ConnectionError:
                self._logger.warning("api_status: cannot reach host")
            except requests.exceptions.ReadTimeout:
                self._logger.warning("api_status: read timeout")
            except requests.exceptions.Timeout:
                self._logger.warning("api_status: request timeout")
            except ValueError:
                self._logger.warning("api_status: no_connector")

    def get_connectors(self):
        connectors = requests.get(
            url=self._url,
            auth=HTTPBasicAuth(
                os.getenv("LDAP_USERNAME"), os.getenv("LDAP_PASSWORD")
            ),
            verify=self._verify,
            cert=self._cert,
            timeout=1,
        ).json()

        return connectors

    def get_status(self, connector):
        # get current connector status
        response = requests.get(
            url=f"""{self._url}/{connector}/status""",
            auth=HTTPBasicAuth(
                os.getenv("LDAP_USERNAME"), os.getenv("LDAP_PASSWORD")
            ),
            verify=self._verify,
            cert=self._cert,
            timeout=1,
        )
        return response.json()
