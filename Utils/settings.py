import os
import configparser
from typing import Union


class Settings:
    """Betrekt configuratie-instellingen uit config.ini"""


    def __init__(self):
        self.config = configparser.ConfigParser()
        curr_dir = os.path.dirname(__file__)
        config_file_path = os.path.join(curr_dir, 'config.ini')
        self.config.read(config_file_path)

    def get_logging_path(self):
        return self.config.get('PATHS', 'loggingPath')

    def get_rel_gpx_path(self):
        return self.config.get('PATHS', 'relGPXPath')

    def get_serial_port(self, comm_type):
        return self.config.get('SERIALCOMMUNICATION', 'serialPort' + comm_type)

    def get_baudrate(self, comm_type):
        return int(self.config.get('SERIALCOMMUNICATION', 'baudrate' + comm_type))

    def get_timeout(self) -> Union[float, None]:
        try:
            return float(self.config.get('SERIALCOMMUNICATION', 'timeout'))
        except ValueError:
            return None

    def get_http_host(self) -> str:
        return self.config.get('HTTPSERVER', 'host')

    def get_http_port(self) -> int:
        return int(self.config.get('HTTPSERVER', 'port'))
