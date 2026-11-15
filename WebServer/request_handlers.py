import os
import logging
from aiohttp import web
from datetime import datetime
from WebServer.HTML.forms import main_form
from Application.GPX.gpx_export import export_gpx
from Utils.settings import Settings


class RequestHandlers:
    def __init__(self, model):
        self.model = model

    async def home(self, request):
        return main_form(r'WebServer/HTML/main.html', self.model)

    async def handle_download(self, request):
        # Pad naar het bestand dat je wilt laten downloaden
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), Settings().get_rel_gpx_path())
        trip_name = "trip" + datetime.now().strftime("%d%m%y")
        file_name = os.path.join(file_path, trip_name + ".gpx")
        if not os.path.exists(file_path):
            return web.Response(text=f"Directory {file_path} niet gevonden", status=404)
        export_gpx(self.model.locations, trip_name, file_name)
        logging.debug(f"Downloading {file_name}")

        # Logische return voor download: web.FileResponse
        # 'headers' dwingen de browser om het bestand op te slaan onder een specifieke naam
        return web.FileResponse(path=file_name, headers={'Content-Disposition': f'attachment; filename="{file_name}"'})

    async def handle_stop(self, request):
        # Logica om de acquisitie stop te zetten
        print("Acquisitie wordt gestopt...")
        # Voer hier je stop-logica uit

        # Logische return voor een actie: Redirect terug naar de hoofdpagina
        raise web.HTTPFound(location='/')
