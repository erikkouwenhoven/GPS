class nmeaRMCMessage:

    """"
    http://home.pacific.net.au/~gnb/gps/nmea.html
    $GPGLL: Geographic Position, Latitude / Longitude and time.

    eg1. $GPGLL,3751.65,S,14507.36,E*77
    eg2. $GPGLL,4916.45,N,12311.12,W,225444,A


               4916.46,N    Latitude 49 deg. 16.45 min. North
               12311.12,W   Longitude 123 deg. 11.12 min. West
               225444       Fix taken at 22:54:44 UTC
               A            Data valid


    eg3. $GPGLL,5133.81,N,00042.25,W*75
                   1    2     3    4 5

          1    5133.81   Current latitude
          2    N         North/South
          3    00042.25  Current longitude
          4    W         East/West
          5    *75       checksum
    $--GLL,lll.ll,a,yyyyy.yy,a,hhmmss.ss,A llll.ll = Latitude of position

    a = N or S
    yyyyy.yy = Longitude of position
    a = E or W
    hhmmss.ss = UTC of position
    A = status: A = valid data
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
        gpsData.setTimeOfFix(item)
        res = rem.split(b',', 1)
        item, rem = res[0], res[1]
        gpsData.setFixValidity(True if item == b'A' else False)
        res = rem.split(b',', 1)
        item, rem = res[0], res[1]
        gpsData.setLatitudeDegrees(item)
        res = rem.split(b',', 1)
        item, rem = res[0], res[1]
        gpsData.setLatitudeHemisphere(item)
        res = rem.split(b',', 1)
        item, rem = res[0], res[1]
        gpsData.setLongitudeDegrees(item)
        res = rem.split(b',', 1)
        item, rem = res[0], res[1]
        gpsData.setLongitudeHemisphere(item)
        res = rem.split(b',', 1)
        item, rem = res[0], res[1]
        gpsData.setSOGinKnots(item)
        res = rem.split(b',', 1)
        item, rem = res[0], res[1]
        res = rem.split(b',', 1)
        item, rem = res[0], res[1]
        gpsData.setDateOfFix(item)


