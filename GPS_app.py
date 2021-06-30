import os
import logging
from logging.handlers import RotatingFileHandler
from Comm.serial_reader import Serial_reader
from settings import Settings
from Comm.Messages.NMEA0183_interpreter import NMEA0183_interpreter
from Model.GPS_Data import GpsData

class Application:

    def __init__(self):
        self.initializeLogging()
        self.run()

    def initializeLogging(self):
        loggingPath = Settings().getLoggingPath()
        if os.path.exists(loggingPath) is False:
            os.mkdir(loggingPath)
            print("{} created".format(loggingPath))
        filename = os.path.join(loggingPath, "log.txt")
        logging.basicConfig(handlers=[RotatingFileHandler(filename, maxBytes=1000000, backupCount=10)],
                            level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logging.info('Start application')

    def run(self):
        gpsData = GpsData()
        serialReader = Serial_reader()
        nmea0183_interpreter = NMEA0183_interpreter(gpsData)
        while True:
            self.handleSerialBuffer(serialReader, nmea0183_interpreter)

    def handleSerialBuffer(self, serialReader, nmea0183_interpreter):
        line = serialReader.getLine()
        logging.debug("Read data: {}".format(line))
        while line:
            nmea0183_interpreter.feedLine(line)
            line = serialReader.getLine()
            logging.debug("Read data: {}".format(line))


if __name__ == "__main__":
    app = Application()
