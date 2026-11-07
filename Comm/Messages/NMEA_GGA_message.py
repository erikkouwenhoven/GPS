from __future__ import annotations
from Comm.Messages.nmea_message import NMEAMessage


class GGAMessage:

    """"
    http://home.pacific.net.au/~gnb/gps/nmea.html
    $GPGGA: Global Positioning System Fix Data

    eg. $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47

    1. UTC-tijd in uren, minuten en seconden (hhmmss.sss)
    2. Breedtegraad (Latitude) in graden en decimale minuten (ddmm.mmmm)
    3. Noord/Zuid-indicator (N of S)
    4. Lengtegraad (Longitude) in graden en decimale minuten (dddmm.mmmm)
    5. Oost/West-indicator (E of W)
    6. GPS-kwaliteitsindicator:
        • 0 = Ongeldig / geen fix
        • 1 = GPS-fix (SPS)
        • 2 = DGPS-fix
        • 4 = RTK Fixed
        • 5 = RTK Float
    7. Aantal actieve satellieten in gebruik (00 t/m 24+)
    8. HDOP (Horizontal Dilution of Precision) – maatstaf voor de nauwkeurigheid van de horinzontale positie
        • 1 – 2 (Excellent): Optimal satellite spread; high horizontal precision.
        • 2 – 5 (Good): Acceptable accuracy for standard navigation and mapping.
        • Above 5 (Poor): Clustered or insufficient satellites; high risk of large positional errors, requiring multi-GNSS or alternative positioning methods.
    9. Antennehoogte (orthometrische hoogte boven de geoïde)
    10. Eenheid van hoogte (M voor meters)
    11. Geoïdale scheiding (verschil tussen ellipsoïde en de geoïde zeeniveauhoogte) in meters
    12. Leeftijd van DGPS-data (leeg als DGPS niet wordt gebruikt)
    13. ID van het referentiestation
    14. Checksum (beginnend met *, ter controle van de data-integriteit)


    """

    SENTENCE_ID = b'GGA'

    Coding = [
        'FIX_TIMESTAMP',
        'LATITUDE_VALUE',
        'LATITUDE_HEMISPHERE',
        'LONGITUDE_VALUE',
        'LONGITUDE_HEMISPHERE',
        'GPS_QUALITY',
        'NUM_SATELLITES',
        'HOR_DILUTION_OF_PRECISION',
        'HEIGHT',
        'HEIGHT_UNIT',
        'GEOIDAL_SEPARATION',
        'DPGS_AGE',
        'REF_STATION_ID'
    ]

    def __init__(self, line: bytes):
        self.msg = NMEAMessage(line)
        self.items = self.msg.items()

    @property
    def has_fix(self) -> bool | None:
        try:
            if self.items[GGAMessage.Coding.index('GPS_QUALITY')] != 0:
                return True
            return False
        except ValueError:
            return False

    @property
    def num_satellites(self) -> int | None:
        try:
            if num := int(self.items[GGAMessage.Coding.index('NUM_SATELLITES')]):
                return num
            return None
        except ValueError:
            return None

    @property
    def hor_dilution(self) -> float | None:
        try:
            if val := float(self.items[GGAMessage.Coding.index('HOR_DILUTION_OF_PRECISION')]):
                return val
            return None
        except ValueError:
            return None

    @property
    def height(self) -> float | None:
        try:
            if val := float(self.items[GGAMessage.Coding.index('HEIGHT')]):
                return val
            return None
        except ValueError:
            return None

    @property
    def height_unit(self) -> bytes | None:
        try:
            if unit := self.items[GGAMessage.Coding.index('HEIGHT_UNIT')]:
                return unit
            return None
        except ValueError:
            return None
