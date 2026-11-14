import logging
import os
from aiohttp import web
from bs4 import BeautifulSoup
from datetime import datetime
from Application.GPX.gpx_export import export_gpx
from Application.model import Model
from Utils.convert_speed import kmh_to_knots
from Utils.settings import Settings
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
            return main_form(r'WebServer/HTML/main.html', self.model)

        @routes.get('/download')
        async def handle_download(request):
            # Pad naar het bestand dat je wilt laten downloaden
            file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), Settings().get_rel_gpx_path(),
                                     "trip" + datetime.now().strftime("%d%m%y") + ".gpx")
            if not os.path.exists(file_path):
                return web.Response(text="Bestand niet gevonden", status=404)
            export_gpx(self.model.locations, file_path)

            # Logische return voor download: web.FileResponse
            # 'headers' dwingen de browser om het bestand op te slaan onder een specifieke naam
            filename = os.path.basename(file_path)
            return web.FileResponse(path=file_path, headers={'Content-Disposition': f'attachment; filename="{filename}"'})

        @routes.post('/stop')
        async def handle_stop(request):
            # Logica om de acquisitie stop te zetten
            print("Acquisitie wordt gestopt...")
            # Voer hier je stop-logica uit

            # Logische return voor een actie: Redirect terug naar de hoofdpagina
            raise web.HTTPFound(location='/')

        @routes.post('/')
        async def _(request):
            data = await request.post()
            return main_form(r'WebServer/HTML/main.html', self.model)

        web_app.add_routes(routes)

        # --- Configure AppRunner instead of web.run_app() ---
        self.runner = web.AppRunner(web_app)
        await self.runner.setup()
        # site = web.TCPSite(self.runner, host=Settings().get_http_host(), port=Settings().get_http_port())
        site = web.TCPSite(self.runner, "0.0.0.0", port=Settings().get_http_port())
        await site.start()
        print(f"Web server started at http://{Settings().get_http_host()}:{Settings().get_http_port()}")

    async def stop_server(self):
        await self.runner.cleanup()
        self.runner = None


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
