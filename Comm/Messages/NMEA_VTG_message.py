from __future__ import annotations
from Utils.convert_speed import kmh_to_knots
from Comm.Messages.nmea_message import NMEAMessage


class VTGMessage:

    """"
    http://home.pacific.net.au/~gnb/gps/nmea.html
    $GPVTG: Track Made Good and Ground Speed.

    eg1. $GPVTG,360.0,T,348.7,M,000.0,N,000.0,K*43
    # eg2. $GPVTG,054.7,T,034.4,M,005.5,N,010.2,K*41


               054.7,T      True course made good over ground, degrees
               034.4,M      Magnetic course made good over ground, degrees
               005.5,N      Ground speed, N=Knots
               010.2,K      Ground speed, K=Kilometers per hour
    """

    SENTENCE_ID = b'VTG'

    Coding = [
        'TRUE_COURSE_VALUE',
        'TRUE_COURSE_LABEL',
        'MAGN_COURSE_VALUE',
        'MAGN_COURSE_LABEL',
        'SPEED_KNOTS_VALUE',
        'SPEED_KNOTS_LABEL',
        'SPEED_KMH_VALUE',
        'SPEED_KMH_LABEL'
    ]

    def __init__(self, line: bytes):
        self.msg = NMEAMessage(line)
        self.items = self.msg.items()

    @classmethod
    def from_speed(cls, speed: float, unit_knots: bool = True) -> VTGMessage:
        speed_knots = speed if unit_knots else speed * kmh_to_knots
        speed_kmh = speed if not unit_knots else speed / kmh_to_knots
        msg = NMEAMessage(f"$GPVTG,360.0,T,348.7,M,{speed_knots:05.1f},N,{speed_kmh:05.1f},K*43".encode())
        assert (updated_msg := msg.update_check_sum())
        return VTGMessage(updated_msg.sentence)

    def is_complete(self) -> bool:
        if self.true_course and self.magnetic_course and self.speed_knots and self.speed_kmh:
            return True
        return False

    @property
    def true_course(self) -> float | None:
        try:
            if (true_course := float(self.items[VTGMessage.Coding.index('TRUE_COURSE_VALUE')])) and self.items[VTGMessage.Coding.index('TRUE_COURSE_LABEL')] == 'T':
                return true_course
            return None
        except (ValueError, IndexError):
            return None

    @property
    def magnetic_course(self) -> float | None:
        try:
            if (magnetic_course := float(self.items[VTGMessage.Coding.index('MAGN_COURSE_VALUE')])) and self.items[VTGMessage.Coding.index('MAGN_COURSE_LABEL')] == 'M':
                return magnetic_course
            return None
        except (ValueError, IndexError):
            return None

    @property
    def speed_knots(self) -> float | None:
        try:
            if (speed_knots := float(self.items[VTGMessage.Coding.index('SPEED_KNOTS_VALUE')])) and self.items[VTGMessage.Coding.index('SPEED_KNOTS_LABEL')] == 'N':
                return speed_knots
            return None
        except (ValueError, IndexError):
            return None

    @property
    def speed_kmh(self) -> float | None:
        try:
            if (speed_kmh := float(self.items[VTGMessage.Coding.index('SPEED_KMH_VALUE')])) and self.items[VTGMessage.Coding.index('SPEED_KMH_LABEL')] == 'K':
                return speed_kmh
            return None
        except (ValueError, IndexError):
            return None
