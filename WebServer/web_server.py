import logging
from aiohttp import web
from Application.model import Model
from Utils.settings import Settings
from WebServer.request_handlers import RequestHandlers


class WebServer:
    def __init__(self, model: Model):
        self.model = model
        self.runner: web.AppRunner | None = None

    async def start_server(self):
        req_handler = RequestHandlers(self.model)
        routes = [
            web.get('/', req_handler.home),
            web.get('/download', req_handler.handle_download),
            web.post('/stop', req_handler.handle_stop),
        ]
        web_app = web.Application()
        web_app.add_routes(routes)

        # --- Configure AppRunner instead of web.run_app() ---
        self.runner = web.AppRunner(web_app)
        await self.runner.setup()
        # site = web.TCPSite(self.runner, host=Settings().get_http_host(), port=Settings().get_http_port())
        site = web.TCPSite(self.runner, "0.0.0.0", port=Settings().get_http_port())
        await site.start()
        logging.debug(f"Web server started at http://{Settings().get_http_host()}:{Settings().get_http_port()}")

    async def stop_server(self):
        await self.runner.cleanup()
        self.runner = None
