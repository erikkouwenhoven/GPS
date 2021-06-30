class nmeaRMCMessage:

    """"
    http://home.pacific.net.au/~gnb/gps/nmea.html
    $GPGSV: GPS Satellites in view

    eg. $GPGSV,3,1,11,03,03,111,00,04,15,270,00,06,01,010,00,13,06,292,00*74
        $GPGSV,3,2,11,14,25,170,00,16,57,208,39,18,67,296,40,19,40,246,00*74
        $GPGSV,3,3,11,22,42,067,42,24,14,311,43,27,05,244,00,,,,*4D


        $GPGSV,1,1,13,02,02,213,,03,-3,000,,11,00,121,,14,13,172,05*62


    1    = Total number of messages of this type in this cycle
    2    = Message number
    3    = Total number of SVs in view
    4    = SV PRN number
    5    = Elevation in degrees, 90 maximum
    6    = Azimuth, degrees from true north, 000 to 359
    7    = SNR, 00-99 dB (null when not tracking)
    8-11 = Information about second SV, same as field 4-7
    12-15= Information about third SV, same as field 4-7
    16-19= Information about fourth SV, same as field 4-7
    """

    c_N_ITEMS = 12

    def __init__(self, line, gpsData):
        if line.count(b',') != self.c_N_ITEMS:
            print("aantal komma's = {}".format(line.count(b',')))
        else:
            self.updateData(line, gpsData)

    def updateData(self, line, gpsData):
        rem = line.split(b',', 1)[1]
        res = rem.split(b',', 1)
        item, rem = res[0], res[1]
