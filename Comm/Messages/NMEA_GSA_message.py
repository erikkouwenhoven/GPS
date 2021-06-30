class nmeaRMCMessage:

    """"
    http://home.pacific.net.au/~gnb/gps/nmea.html
    $GPGSA: GPS DOP and active satellites

    eg1. $GPGSA,A,3,,,,,,16,18,,22,24,,,3.6,2.1,2.2*3C
    eg2. $GPGSA,A,3,19,28,14,18,27,22,31,39,,,,,1.7,1.0,1.3*34


    1    = Mode:
           M=Manual, forced to operate in 2D or 3D
           A=Automatic, 3D/2D
    2    = Mode:
           1=Fix not available
           2=2D
           3=3D
    3-14 = PRN's of Satellite Vechicles (SV's) used in position fix (null for unused fields)
    15   = Position Dilution of Precision (PDOP)
    16   = Horizontal Dilution of Precision (HDOP)
    17   = Vertical Dilution of Precision (VDOP)
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
