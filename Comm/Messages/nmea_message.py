from __future__ import annotations


class NMEAMessage:
    """
        http://home.pacific.net.au/~gnb/gps/nmea.html
        $GPGGA: Global Positioning System Fix Data

    Representeert een NMEA-message (in bytes, vanwege de seriële overdracht). De string is als volgt opgebouwd:

            Voorbeeld: $VWMTW,16.5,C*10\r\n
            Start met $-teken
            Talker id: eerste twee karakters
            Sentence id: volgende 3 karakters
            Sentence zelf, bevat de info gescheiden door komma's
            Eindigt met *-teken
            Checksum, twee hex-karakters. De karakters tussen $ en * worden met elkaar ge-XOR-d
            Eventueel CR, LF

    """

    def __init__(self, message: bytes):
        self.message = message

    def talker_id(self):
        try:
            return self.message[1:3]
        except IndexError:
            return None

    def sentence_id(self) -> bytes | None:
        try:
            return self.message[3:6]
        except IndexError:
            return None

    def isolate_checksum(self) -> bytes | None:
        try:
            i_end = self.message.find(b'*')
        except ValueError:
            return None
        return self.message[i_end + 1:].strip()

    def is_consistent(self) -> bool:
        if self.isolate_checksum() == self.calculate_check_sum():
            return True
        else:
            return False

    def isolate_bare_message(self) -> bytes | None:
        try:
            i_start = self.message.index(b'$')
            i_end = self.message.find(b'*')
        except ValueError:
            return None
        if i_start > i_end:
            return None
        return self.message[i_start + 1:i_end]

    def calculate_check_sum(self) -> bytes | None:
        if bare_msg := self.isolate_bare_message():
            calc_checksum = 0
            for s in bare_msg:
                calc_checksum ^= s
            return f"{calc_checksum:02X}".encode()
        else:
            return None

    def update_check_sum(self) -> NMEAMessage | None:
        try:
            i_end = self.message.find(b'*')
        except ValueError:
            return None
        self.message = self.message[:i_end + 1] + self.calculate_check_sum()
        return self

    def __repr__(self):
        return str(self.message)
