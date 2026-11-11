class Location:
    """
    Locatie op de wereldbol. Constructor accepteert NMEA01830 conventie:

        4916.45,N    Latitude 49 deg. 16.45 min North
        12311.12,W   Longitude 123 deg. 11.12 min West

        Latitude can be both positive and negative, depending on which hemisphere the location is in:
        • Positive (+) latitudes are located in the Northern Hemisphere (north of the equator, from 0° to +90°).
        • Negative (-) latitudes are located in the Southern Hemisphere (south of the equator, from 0° to -90°).
        • Zero (0°) is right on the equator.

        Longitude:
        • Positive (+): East (e.g., 4.3° E is positive)
        • Negative (-): West (e.g., 74° W is negative)
        • Range: Values run from -180° to +180°.

    Intern wordt het opgeslagen als floats
    """
    def __init__(self, lat_str: str, lat_hemi: str, long_str: str, long_hemi: str):
        self.latitude: float | None = Location.from_nmea0183(lat_str)
        self.longitude: float | None = Location.from_nmea0183(long_str)
        if lat_hemi != 'N' and self.latitude:
            self.latitude = -self.latitude
        if long_hemi != 'E' and self.longitude:
            self.longitude = -self.longitude

    @staticmethod
    def from_nmea0183(in_str: str) -> float | None:
        # 2 karakters voor de decimale punt zijn voor de minuten
        if (dec_pt := in_str.find('.')) != -1:
            try:
                val_deg = float(in_str[:dec_pt - 2])
                val_min = float(in_str[dec_pt - 2:])
            except ValueError:
                return None
            return val_deg + val_min / 60.0
        else:
            return None

    def __repr__(self):
        return (f"LAT: {abs(self.latitude):.3f} {'N' if self.latitude > 0.0 else 'S'}, "
                f"LONG: {abs(self.longitude):.3f} {'E' if self.latitude > 0.0 else 'W'}")
