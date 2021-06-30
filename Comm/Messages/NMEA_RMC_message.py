class nmeaRMCMessage:

    """"
    http://home.pacific.net.au/~gnb/gps/nmea.html
    $GPRMC: Recommended minimum specific GPS/TRANSIT data

    eg1. $GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62
    eg2. $GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68


               225446       Time of fix 22:54:46 UTC
               A            Navigation receiver warning A = Valid position, V = Warning
               4916.45,N    Latitude 49 deg. 16.45 min. North
               12311.12,W   Longitude 123 deg. 11.12 min. West
               000.5        Speed over ground, Knots
               054.7        Course Made Good, degrees true
               191194       UTC Date of fix, 19 November 1994
               020.3,E      Magnetic variation, 20.3 deg. East
               *68          mandatory checksum
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


