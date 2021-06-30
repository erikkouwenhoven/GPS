import datetime
import time

class GpsData:

    def __init__(self):
        self.fixDateTime = None
        self.validFix = False
        self.LatitudeDegrees = None
        self.LatitudeHemisphere = None
        self.LongitudeDegrees = None
        self.LongitudeHemisphere = None
        self.sogInKnots = None

    def setTimeOfFix(self, value):
        if not self.fixDateTime:
            self.fixDateTime = datetime.datetime.now()
        self.fixDateTime.replace(hour=value[0:2], minute=value[2:4], second=value[4:6])

    def setFixValidity(self, value):
        self.validFix = value

    def setLatitudeDegrees(self, value):
        self.LatitudeDegrees = value

    def setLatitudeHemisphere(self, value):
        self.LatitudeHemisphere = value

    def setLongitudeDegrees(self, value):
        self.LongitudeDegrees = value

    def setLongitudeHemisphere(self, value):
        self.LongitudeHemisphere = value

    def setSOGinKnots(self, value):
        self.sogInKnots = value

    def setDateOfFix(self, value):
        if not self.fixDateTime:
            self.fixDateTime = datetime.datetime.now()
        self.fixDateTime.replace(day=value[0:2], month=value[2:4], year=value[4:6])

    def __str__(self):
        S = "Fix: {}".format(self.validFix)
        S += "Fix time: {}".format(self.fixDateTime)
        S += "Lat: {}".format(self.LatitudeDegrees)
        return S
