import logging
from aiohttp import web
from bs4 import BeautifulSoup


def html_response(document):
    s = open(document, "r")
    html = s.read()
    soup = BeautifulSoup(html, 'html.parser')
    fix_date_time_label = soup.find(id="fix_date_time")
    fix_date_time_label.string = "modified"
    return web.Response(text=soup.prettify(), content_type='text/html')


async def start_server():
    # --- Create the aiohttp Application ---
    web_app = web.Application()
    routes = web.RouteTableDef()

    @routes.get('/')
    async def index_handler(request):
        return html_response(r'WebServer\HTML\main.html')

    web_app.add_routes(routes)

    # --- Configure AppRunner instead of web.run_app() ---
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, host='Dell_16', port=8080)
    await site.start()
    print("Web server started at http://Dell_16:8080")
