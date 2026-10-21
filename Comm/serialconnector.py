import serial
import logging
from settings import Settings


class SerialConnector:

    def __init__(self):
        self.ser = None
        try:
            settings = Settings()
            self.ser = serial.Serial(
                port=settings.getSerialPort(),
                baudrate=settings.getBaudrate(),
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=settings.getTimeout()
            )
            logging.debug(self.ser)
        except serial.SerialException as e:
            logging.error("SerialException: " + str(e))

    def get_line(self) -> bytes | None:
        try:
            line = self.ser.readline()
            logging.debug(line)
        except serial.SerialException as e:
            logging.error("SerialException: " + str(e))
            return None
        return line if len(line) > 0 else None

    def put_line(self, line: bytes):
        try:
            self.ser.write(line)
            logging.debug(f"wrote {line}")
        except serial.SerialException as e:
            logging.error("SerialException: " + str(e))
            return None
