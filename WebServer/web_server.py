import logging
from aiohttp import web
from bs4 import BeautifulSoup
from datetime import datetime
from Application.model import Model
from Utils.convert_speed import kmh_to_knots
from Utils.utils import pretty_time_diff


class WebServer:
    def __init__(self, model: Model):
        self.model = model
        self.runner: web.AppRunner | None = None

    async def start_server(self):
        # --- Create the aiohttp Application ---
        web_app = web.Application()
        routes = web.RouteTableDef()

        @routes.get('/')
        async def _(request):
            return main_form(r'WebServer\HTML\main.html', self.model)

        web_app.add_routes(routes)

        # --- Configure AppRunner instead of web.run_app() ---
        self.runner = web.AppRunner(web_app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, host='Dell_16', port=8080)
        await site.start()
        print("Web server started at http://Dell_16:8080")

    async def stop_server(self):
        await self.runner.cleanup()
        self.runner = None


def main_form(document: str, model: Model):
    s = open(document, "r")
    soup = BeautifulSoup(s.read(), 'html.parser')
    running_since_label = soup.find(id="running_since")
    running_since_label.string = pretty_time_diff(model.start_time_stamp, datetime.now().timestamp())
    fix_date_time_label = soup.find(id="fix_date_time")
    fix_date_time_label.string = model.fix_datetime.strftime("%d/%m/%Y, %H:%M:%S") if model.fix_datetime else "NO FIX"
    speed_label = soup.find(id="speed")
    speed_label.string = f"{model.speed_knots:.2f} knots {model.speed_knots / kmh_to_knots:.2f} km/h"
    location_label = soup.find(id="position")
    location_label.string = f"{model.location}"
    satellites_label = soup.find(id="satellites")
    satellites_label.string = f"{model.num_satellites}"
    height_label = soup.find(id="height")
    height_label.string = f"{model.height}"
    height_unit_label = soup.find(id="height_unit")
    height_unit_label.string = f"{model.height_unit.decode('utf8')}"
    hor_dilution_label = soup.find(id="hor_dilution")
    hor_dilution_label.string = f"{model.hor_dilution}"

    return web.Response(text=soup.prettify(), content_type='text/html')
