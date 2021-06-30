import logging
from Comm.Messages.NMEA_RMC_message import nmeaRMCMessage


class NMEA0183_interpreter:

    def __init__(self, gpsData):
        self.gpsData = gpsData

    def feedLine(self, line):
        if self.isValid(line) is True:
            if self.checkSum(line) is True:
                self.parse(line)
        else:
            logging.info("Invalid line: {}".format(line))

    def isValid(self, line):
        """Check validity:
        eerste record start met $
        """
        try:
            ident = line.split(b',')[0]
        except IndexError:
            return False
        if len(ident) != 6:
            return False
        if chr(ident[0]) != '$':
            return False
        return True

    def checkSum(self, line):
        nmeadata, cksum = line[1:].split(b'*')
        calc_cksum = 0
        for s in nmeadata:
            calc_cksum ^= s
        return int(cksum[:2], 16) == int(calc_cksum)

    def parse(self, line):
        msgType = line[3:6]
        if msgType == b'RMC':
            msg = nmeaRMCMessage(line, self.gpsData)
        elif msgType == b'VTG':
            pass
        elif msgType == b'GGA':
            pass
        elif msgType == b'GSA':
            pass
        elif msgType == b'GSV':
            pass
        elif msgType == b'GLL':
            pass
        pass
