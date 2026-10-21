from __future__ import annotations
from Comm.Messages.convert_speed import kmh_to_knots
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

    def __init__(self, line: bytes):
        self.msg = NMEAMessage(line)

    @classmethod
    def from_speed(cls, speed: float, unit_knots: bool = True) -> VTGMessage:
        speed_knots = speed if unit_knots else speed * kmh_to_knots
        speed_kmh = speed if not unit_knots else speed / kmh_to_knots
        msg = f"$GPVTG,360.0,T,348.7,M,{speed_knots:05.1f},N,{speed_kmh:05.1f},K*43".encode()
        return VTGMessage(NMEAMessage(msg).update_check_sum().message)
