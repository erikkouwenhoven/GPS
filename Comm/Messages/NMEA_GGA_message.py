class nmeaRMCMessage:

    """"
    http://home.pacific.net.au/~gnb/gps/nmea.html
    $GPGGA: Global Positioning System Fix Data

    eg1. $GPGGA,170834,4124.8963,N,08151.6838,W,1,05,1.5,280.2,M,-34.0,M,,,*75

    Name	Example Data	Description
    Sentence Identifier	$GPGGA	Global Positioning System Fix Data
    Time	170834	17:08:34 UTC
    Latitude	4124.8963, N	41d 24.8963' N or 41d 24' 54" N
    Longitude	08151.6838, W	81d 51.6838' W or 81d 51' 41" W
    Fix Quality:
    - 0 = Invalid
    - 1 = GPS fix
    - 2 = DGPS fix	1	Data is from a GPS fix
    Number of Satellites	05	5 Satellites are in view
    Horizontal Dilution of Precision (HDOP)	1.5	Relative accuracy of horizontal position
    Altitude	280.2, M	280.2 meters above mean sea level
    Height of geoid above WGS84 ellipsoid	-34.0, M	-34.0 meters
    Time since last DGPS update	blank	No last update
    DGPS reference station id	blank	No station id
    Checksum	*75	Used by program to check for transmission errors
    Courtesy of Brian McClure, N8PQI.

    Global Positioning System Fix Data. Time, position and fix related data for a GPS receiver.

    eg2. $GPGGA,hhmmss.ss,ddmm.mmm,a,dddmm.mmm,b,q,xx,p.p,a.b,M,c.d,M,x.x,nnnn

    hhmmss.ss = UTC of position
    ddmm.mmm = latitude of position
    a = N or S, latitutde hemisphere
    dddmm.mmm = longitude of position
    b = E or W, longitude hemisphere
    q = GPS Quality indicator (0=No fix, 1=Non-differential GPS fix, 2=Differential GPS fix, 6=Estimated fix)
    xx = number of satellites in use
    p.p = horizontal dilution of precision
    a.b = Antenna altitude above mean-sea-level
    M = units of antenna altitude, meters
    c.d = Geoidal height
    M = units of geoidal height, meters
    x.x = Age of Differential GPS data (seconds since last valid RTCM transmission)
    nnnn = Differential reference station ID, 0000 to 1023
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
