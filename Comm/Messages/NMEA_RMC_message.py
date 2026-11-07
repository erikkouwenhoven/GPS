from __future__ import annotations
from datetime import datetime
import pytz
from Utils.location import Location
from Comm.Messages.nmea_message import NMEAMessage


class RMCMessage:

    """"
    http://home.pacific.net.au/~gnb/gps/nmea.html
    $GPRMC: Recommended Minimum Specific GNSS Data

    eg. $GPRMC,161335.00,A,5210.28418,N,00423.99276,E,0.432,,271026,,,A*71

        161335.00           UTC-tijd van de fix
        A                   Status (A: data geldig, V: warning)
        5210.28418,N        Breedtegraad
        00423.99276,E       Lengtegraad
        0.432               Snelheid in knopen
        -                   Koers
        271026              Datum van fix
        -                   Magnetische var. en de richting daarvan
        Modus-indicator     A = Autonomous
    """

    SENTENCE_ID = b'RMC'

    Coding = [
        'FIX_TIMESTAMP',
        'FIX_STATUS',
        'LATITUDE_VALUE',
        'LATITUDE_HEMISPHERE',
        'LONGITUDE_VALUE',
        'LONGITUDE_HEMISPHERE',
        'SPEED_KNOTS_VALUE',
        'COURSE',
        'FIX_DATE',
        'MAGN_VAR_VALUE',
        'MAGN_VAR_DIRECTION',
        'MODUS'
    ]

    def __init__(self, line: bytes):
        self.msg = NMEAMessage(line)
        self.items = self.msg.items()

    def is_complete(self) -> bool:
        if self.true_course and self.magnetic_course and self.speed_knots and self.speed_kmh:
            return True
        return False

    @property
    def has_fix(self) -> bool | None:
        try:
            if self.items[RMCMessage.Coding.index('FIX_STATUS')] == b'A':
                return True
            return False
        except ValueError:
            return False

    @property
    def fix_datetime(self) -> datetime | None:
        try:
            if (fix_time := self.items[RMCMessage.Coding.index('FIX_TIMESTAMP')]) and (fix_date := self.items[RMCMessage.Coding.index('FIX_DATE')]):
                timestamp = datetime.strptime((fix_date + fix_time[:-3]).decode(encoding='utf-8'), '%d%m%y' + '%H%M%S')
                utc_dt = pytz.utc.localize(timestamp).astimezone(pytz.timezone("Europe/Amsterdam"))
                return utc_dt
            else:
                return None
        except ValueError:
            return None

    @property
    def location(self) -> Location | None:
        if (long_val := self.items[RMCMessage.Coding.index('LONGITUDE_VALUE')].decode(encoding='utf-8')) and\
                (long_hemi := self.items[RMCMessage.Coding.index('LONGITUDE_HEMISPHERE')].decode(encoding='utf-8')) and\
                (lat_val := self.items[RMCMessage.Coding.index('LATITUDE_VALUE')].decode(encoding='utf-8')) and\
                (lat_hemi := self.items[RMCMessage.Coding.index('LATITUDE_HEMISPHERE')].decode(encoding='utf-8')):
            return Location(lat_val, lat_hemi, long_val, long_hemi)
        else:
            return None

    @property
    def true_course(self) -> float | None:
        try:
            if true_course := float(self.items[RMCMessage.Coding.index('COURSE')]):
                return true_course
            return None
        except ValueError:
            return None

    @property
    def magnetic_course(self) -> float | None:
        try:
            if (magnetic_course := float(self.items[RMCMessage.Coding.index('MAGN_COURSE_VALUE')])) and self.items[RMCMessage.Coding.index('MAGN_COURSE_LABEL')] == 'M':
                return magnetic_course
            return None
        except ValueError:
            return None

    @property
    def speed_knots(self) -> float | None:
        try:
            if speed_knots := float(self.items[RMCMessage.Coding.index('SPEED_KNOTS_VALUE')]):
                return speed_knots
            return None
        except ValueError:
            return None
