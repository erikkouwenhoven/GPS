import os
import datetime
import configparser


class Settings:
    """Betrekt configuratie-instellingen uit config.ini"""


    def __init__(self):
        self.config = configparser.ConfigParser()
        currDir = os.path.dirname(os.path.dirname(__file__))
        configFilePath = currDir + r'\config.ini'
        self.config.read(configFilePath)

    def getLoggingPath(self):
        return self.config.get('PATHS', 'loggingPath')

    def getSerialPort(self):
        return self.config.get('COMMUNICATION', 'serialPort')

    def getBaudrate(self):
        return self.config.get('COMMUNICATION', 'baudrate')

    def getTimeout(self):
        return self.config.get('COMMUNICATION', 'timeout')

