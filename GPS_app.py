import os
import logging
from logging.handlers import RotatingFileHandler
from Comm.Messages.NMEA_VTG_message import VTGMessage
from Comm.Messages.nmea_message import NMEAMessage
from Comm.serialconnector import SerialConnector
from settings import Settings

class Application:

    def __init__(self):
        self.initializeLogging()
        print(NMEAMessage(b'$VWMTW,16.5,C*10\r\n').calculate_check_sum())
        print(NMEAMessage(b'$VWMTW,16.5,C*10\r\n').isolate_checksum())
        print(NMEAMessage(b'$VWMTW,16.5,C*10\r\n').isolate_bare_message())
        print(NMEAMessage(b'$VWMTW,16.5,C*10\r\n').is_consistent())
        print(NMEAMessage(b'$GPVTG,360.0,T,348.7,M,000.0,N,000.0,K*43').is_consistent())
        print(VTGMessage.from_speed(1).msg)
        print(VTGMessage.from_speed(1).msg.is_consistent())

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
        speed = 0.0
        serial_connector = SerialConnector()
        if serial_connector.ser:
            while True:
                while line := serial_connector.get_line():
                    logging.debug(f"Read data: {line}")
                    print(f"Read data: {line} type={NMEAMessage(line).sentence_id()}")

                vtg_msg = VTGMessage.from_speed(speed)
                serial_connector.put_line(vtg_msg.message)
                speed += 0.1
        else:
            print("No serial connector")

if __name__ == "__main__":
    app = Application()

# stoppen en reader afsluiten (close port)
# setje van inputregels lezen
