from Comm.Messages.nmea_message import NMEAMessage


class MTWMessage:
    """
    In boordelektronica op schepen is $VWMTW de standaardcode waarmee een sensor de watertemperatuur naar een kaartplotter
    of instrument verstuurt.
    Voorbeeld b'$VWMTW,16.5,C*10\r\n'

    •	VW (Talker ID): Staat nog steeds voor uw mechanische snelheidssensor of speed log (Velocity sensor, water,
        mechanical). Veel moderne loggevers hebben namelijk ook een ingebouwde temperatuursensor.
    •	MTW (Sentence ID): Staat voor Water Temperature (Watertemperatuur).
    •	16.5: De gemeten waarde.
    •	C: De eenheid, in dit geval Celsius.
    """

    SENTENCE_ID = b'MTW'

    Coding = [
        'TEMP_VALUE',
        'TEMP_UNIT'
    ]

    def __init__(self, line: bytes):
        self.msg = NMEAMessage(line)
        self.items = self.msg.items()

    @property
    def temp_in_celsius(self) -> float | None:
        try:
            if (temp_in_celsius := float(self.items[MTWMessage.Coding.index('TEMP_VALUE')])) and self.items[
                MTWMessage.Coding.index('TEMP_UNIT')] == 'C':
                return temp_in_celsius
            return None
        except (ValueError, IndexError):
            return None
