from aiohttp import web
from bs4 import BeautifulSoup
from datetime import datetime
from Application.model import Model
from Utils.convert_speed import kmh_to_knots
from Utils.utils import pretty_time_diff


def main_form(document: str, model: Model):
    s = open(document, "r")
    soup = BeautifulSoup(s.read(), 'html.parser')

    if serial_connection_label := soup.find(id="serial_connection"):
        serial_connection_label.string = ",".join(f"{key}: {val}" for key, val in model.is_running_connector.items())

    if running_since_label := soup.find(id="running_since"):
        running_since_label.string = pretty_time_diff(model.start_time_stamp, datetime.now().timestamp())

    if fix_date_time_label := soup.find(id="fix_date_time"):
        fix_date_time_label.string = model.fix_datetime.strftime("%d/%m/%Y, %H:%M:%S") if model.fix_datetime else "NO FIX"

    if speed_label := soup.find(id="speed"):
        if model.speed_knots:
            speed_label.string = f"{model.speed_knots:.2f} knots {model.speed_knots / kmh_to_knots:.2f} km/h"

    if location_label := soup.find(id="position"):
        location_label.string = f"{model.location}"

    if satellites_label := soup.find(id="satellites"):
        satellites_label.string = f"{model.num_satellites}"

    if height_label := soup.find(id="height"):
        height_label.string = f"{model.height}"
    if (height_unit_label := soup.find(id="height_unit")) and (height_unit := model.height_unit):
        height_unit_label.string = f"{height_unit.decode('utf8')}"

    if hor_dilution_label := soup.find(id="hor_dilution"):
        hor_dilution_label.string = f"{model.hor_dilution}"

    if speed_water_label := soup.find(id="speed_water"):
        speed_water_label.string = f"{model.water_speed_knots} knots"

    if water_temp_label := soup.find(id="water_temp"):
        water_temp_label.string = f"{model.water_temp} C"

    if trip_label := soup.find(id="trip"):
        trip_label.string = f"{model.curr_dist_in_nm} nm"

    if total_label := soup.find(id="total"):
        total_label.string = f"{model.total_dist_in_nm} nm"

    return web.Response(text=soup.prettify(), content_type='text/html')
