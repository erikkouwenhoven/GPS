import serial
import logging
from settings import Settings


class Serial_reader:

    def __init__(self):
        self._ser = None
        try:
            settings = Settings()
            self._ser = serial.Serial(
                port=settings.getSerialPort(),
                baudrate=settings.getBaudrate(),
                timeout=settings.getTimeout()
            )
        except serial.SerialException as e:
            logging.error("SerialException: " + str(e))

    def getLine(self):
        try:
            line = self._ser.readline()
            logging.debug(line)
        except serial.SerialException as e:
            logging.error("SerialException: " + str(e))
            return None
        return line
