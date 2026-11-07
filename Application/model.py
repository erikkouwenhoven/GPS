from datetime import datetime
from Utils.location import Location


class Model:

    def __init__(self):
        self.start_time_stamp: float = datetime.now().timestamp()
        self.fix_datetime: datetime | None = None
        self.last_reading_timestamp: datetime | None = None
        self.speed_knots: float | None = None
        self.location: Location | None = None
        self.num_satellites: int | None = None
        self.height: float | None = None
        self.height_unit: bytes | None = None
        self.hor_dilution: float | None = None

    @property
    def has_fix(self) -> bool:
        return self.fix_datetime is not None

    def set_fix_datetime(self, fix_datetime: datetime):
        self.fix_datetime = fix_datetime

    def set_reading(self, speed_knots: float, location: Location) -> None:
        self.speed_knots = speed_knots
        self.location = location
        self.last_reading_timestamp = datetime.now()

    def set_num_satellites(self, num_satellites):
        self.num_satellites = num_satellites

    def set_height(self, height):
        self.height = height

    def set_height_unit(self, height_unit):
        self.height_unit = height_unit

    def set_hor_dilution(self, hor_dilution):
        self.hor_dilution = hor_dilution
