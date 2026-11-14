from Comm.Messages.nmea_message import NMEAMessage


class VLWMessage:
    """
    Dit is een NMEA 0183-datastring van het type VLW, wat staat voor Distance Traveled Through Water.
    Voorbeeld b'$VWVLW,544.3,N,122.85,N,,,,*76\r\n'

    Betekenis van deze specifieke string:
    •	$VWVLW: De header. VW staat voor de snelheidssensor (Speed Log) en VLW staat voor de logstand (afstand).
    •	544.3,N: De totale afstand (Trip odometer of Total cumulative distance) sinds de sensor in gebruik is genomen
        bedraagt 544,3 zeemijl (N = Nautical miles).
    •	122.85,N: De huidige tripafstand (Distance since reset) bedraagt 122,85 zeemijl (N = Nautical miles). Dit is de
        afstand sinds de laatste handmatige reset van de tripmeter.
    •	,,,,: De overige velden zijn leeg. Bij nieuwere NMEA-versies kunnen hier aanvullende eenheden of waarden staan,
        maar deze worden door uw sensor niet gebruikt.
    •	*76: De checksum om de integriteit van de dataregel te controleren.
    •	\r\n': De standaardaansluiting van een dataregel (Carriage Return en Line Feed).
    """

    SENTENCE_ID = b'VLW'

    Coding = [
        'TOTAL_DIST_VALUE',
        'TOTAL_DIST_UNIT',
        'CURR_DIST_VALUE',
        'CURR_DIST_UNIT'
    ]


    def __init__(self, line: bytes):
        self.msg = NMEAMessage(line)
        self.items = self.msg.items()

    @property
    def total_dist_in_nm(self) -> float | None:
        try:
            if (total_dist_in_nm := float(self.items[VLWMessage.Coding.index('TOTAL_DIST_VALUE')])) and self.items[
                VLWMessage.Coding.index('TOTAL_DIST_UNIT')] == 'N':
                return total_dist_in_nm
            return None
        except (ValueError, IndexError):
            return None

    @property
    def curr_dist_in_nm(self) -> float | None:
        try:
            if (curr_dist_in_nm := float(self.items[VLWMessage.Coding.index('CURR_DIST_VALUE')])) and self.items[
                VLWMessage.Coding.index('CURR_DIST_UNIT')] == 'N':
                return curr_dist_in_nm
            return None
        except (ValueError, IndexError):
            return None
