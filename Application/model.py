from datetime import datetime
from Application.location import Location


class Model:

    def __init__(self) -> None:
        self.start_time_stamp: float = datetime.now().timestamp()
        self.is_running_connector: dict[str, bool] = {}
        self.fix_datetime: datetime | None = None
        self.last_reading_timestamp: datetime | None = None
        self.speed_knots: float | None = None
        self.locations: list[Location] = []
        self.num_satellites: int | None = None
        self.height: float | None = None
        self.height_unit: bytes | None = None
        self.hor_dilution: float | None = None
        self.water_temp: float | None = None
        self.curr_dist_in_nm: float | None = None
        self.total_dist_in_nm: float | None = None
        self.water_speed_knots: float | None = None

    @property
    def has_fix(self) -> bool:
        return self.fix_datetime is not None

    def set_fix_datetime(self, fix_datetime: datetime):
        self.fix_datetime = fix_datetime

    def set_reading(self, speed_knots: float, location: Location) -> None:
        self.speed_knots = speed_knots
        self.locations.append(location)
        self.last_reading_timestamp = datetime.now()

    def set_num_satellites(self, num_satellites):
        self.num_satellites = num_satellites

    def set_height(self, height):
        self.height = height

    def set_height_unit(self, height_unit):
        self.height_unit = height_unit

    def set_hor_dilution(self, hor_dilution):
        self.hor_dilution = hor_dilution

    def set_is_running(self, connector_name: str, is_running: bool) -> None:
        self.is_running_connector[connector_name] = is_running

    def set_water_temp(self, water_temp: float | None) -> None:
        self.water_temp = water_temp

    def set_curr_dist_in_nm(self, curr_dist_in_nm: float | None) -> None:
        self.curr_dist_in_nm = curr_dist_in_nm

    def set_total_dist_in_nm(self, total_dist_in_nm: float | None) -> None:
        self.total_dist_in_nm = total_dist_in_nm

    def set_water_speed_knots(self, water_speed_knots: float | None) -> None:
        self.water_speed_knots = water_speed_knots

    @property
    def location(self) -> Location | None:
        try:
            return self.locations[-1]
        except IndexError:
            return None
