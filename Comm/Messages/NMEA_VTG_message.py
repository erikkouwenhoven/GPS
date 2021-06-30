class nmeaRMCMessage:

    """"
    http://home.pacific.net.au/~gnb/gps/nmea.html
    $GPVTG: Track Made Good and Ground Speed.

    eg1. $GPVTG,360.0,T,348.7,M,000.0,N,000.0,K*43
    eg2. $GPVTG,054.7,T,034.4,M,005.5,N,010.2,K*41


               054.7,T      True course made good over ground, degrees
               034.4,M      Magnetic course made good over ground, degrees
               005.5,N      Ground speed, N=Knots
               010.2,K      Ground speed, K=Kilometers per hour


    eg3. for NMEA 0183 version 3.00 active the Mode indicator field
         is added at the end
         $GPVTG,054.7,T,034.4,M,005.5,N,010.2,K,A*53
               A            Mode indicator (A=Autonomous, D=Differential,
                            E=Estimated, N=Data not valid
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


