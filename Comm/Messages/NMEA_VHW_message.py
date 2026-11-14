from Comm.Messages.nmea_message import NMEAMessage


class VHWMessage:
    """
    VWVHW is a standard NMEA 0183 marine sentence used to transmit water speed and compass heading relative to the water.
    Example: b'$VWVHW,,,,,0.00,N,0.00,K*4D\r\n'

    • Prefix (VW): Identifies the talker ID (typically a dual or water speed/heading sensor, or proprietary/accumulated
        device prefix like VW or GP).
    • VHW: The sentence formatter standing for Water Speed and Heading.
    • Data Fields Included:
        1. Heading (True) in degrees
        2. T (True designator)
        3. Heading (Magnetic) in degrees
        4. M (Magnetic designator)
        5. Speed through the water in knots
        6. N (Knots designator)
        7. Speed through the water in km/h
        8. K (Kilometers per hour designator)
    """

    SENTENCE_ID = b'VHW'

    Coding = [
        'WATER_SPEED_KNOTS_VALUE',
        'WATER_SPEED_KNOTS_LABEL',
        'WATER_SPEED_KMH_VALUE',
        'WATER_SPEED_KMH_LABEL'
    ]


    def __init__(self, line: bytes):
        self.msg = NMEAMessage(line)
        self.items = self.msg.items()

    @property
    def water_speed_knots(self) -> float | None:
        try:
            if (water_speed_knots := float(self.items[VHWMessage.Coding.index('WATER_SPEED_KNOTS_VALUE')])) and\
                self.items[VHWMessage.Coding.index('WATER_SPEED_KNOTS_LABEL')] == 'N':
                return water_speed_knots
            return None
        except (ValueError, IndexError):
            return None

    @property
    def water_speed_kmh(self) -> float | None:
        try:
            if (water_speed_kmh := float(self.items[VHWMessage.Coding.index('WATER_SPEED_KMH_VALUE')])) and\
                    self.items[VHWMessage.Coding.index('WATER_SPEED_KMH_LABEL')] == 'K':
                return water_speed_kmh
            return None
        except (ValueError, IndexError):
            return None
