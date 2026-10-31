import os
import datetime
import configparser


class Settings:
    """Betrekt configuratie-instellingen uit config.ini"""


    def __init__(self):
        self.config = configparser.ConfigParser()
        currDir = os.path.dirname(__file__)
        configFilePath = os.path.join(currDir, 'config.ini')
        self.config.read(configFilePath)

    def getLoggingPath(self):
        currDir = os.path.dirname(__file__)
        configFilePath = currDir + r'\config.ini'
        print(f"{configFilePath}")
        return self.config.get('PATHS', 'loggingPath')

    def getSerialPort(self, comm_type):
        return self.config.get('COMMUNICATION', 'serialPort' + comm_type)

    def getBaudrate(self, comm_type):
        return int(self.config.get('COMMUNICATION', 'baudrate' + comm_type))

    def getTimeout(self) -> float:
        try:
            return float(self.config.get('COMMUNICATION', 'timeout'))
        except ValueError:
            return None
