from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time

# class _MidasServlet(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(bytes(
#             "<html><head><title>Midas</title></head>" +
#             ("<p>Request: %s</p>" % self.path) +
#             "<body>" +
#             "<p>This is an example web server.</p>" +
#             "</body></html>", "utf-8"))
#
#
#
# class MidasServer:
#     def __init__(self, hostName="localhost", serverPort=8080):
#         self.hostName = hostName
#         self.serverPort = serverPort
#         self.webServer = HTTPServer((hostName, serverPort), _MidasServlet)
#         self.thread = None
#
#     def run_in_background(self):
#         if not self.thread:
#             self.thread = threading.Thread(target=lambda : self.run())
#             self.thread.start()
#         return self
#
#     def stop(self):
#         if self.thread:
#             self.webServer.shutdown()
#             self.thread.join()
#
#     def run(self):
#         print("Starting server http://%s:%s" % (self.hostName, self.serverPort))
#
#         try:
#             self.webServer.serve_forever()
#         except KeyboardInterrupt:
#             pass
#
#         self.webServer.server_close()
#         print("Server http://%s:%s stopped." % (self.hostName, self.serverPort))

# ------------------

import sys
import os
import aiohttp
from aiohttp import web, WSCloseCode
import asyncio

# TODO pass this to http_handler() somehow, instead of having global
WEB_DIR = None


async def http_handler(request):
    request_path = request.url.path
    if request_path == '/':
        request_path = '/index.html'
    elif -1 != request_path.find(".."):
        raise web.HTTPNotFound()
    elif -1 != request_path.find("/", 1):
        raise web.HTTPNotFound()
    os_path = WEB_DIR + request_path
    if os.path.exists(os_path):
        return web.FileResponse(os_path)


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str('some websocket message payload')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())

    return ws


async def start_server(host="127.0.0.1", port=1337):
    app = web.Application()
    app.add_routes([
        web.get('/ws', websocket_handler),
        web.get('/{file}', http_handler),
        web.get('/', http_handler),
    ])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()


class MidasServer:
    def __init__(self, hostName="localhost", serverPort=8080):
        global WEB_DIR
        self.hostName = hostName
        self.serverPort = serverPort
        self.thread = None
        self.loop = None
        self.web_server_running = False
        if not WEB_DIR:
            webdir = os.getcwd()
            if webdir.endswith("/static"):
                pass
            elif webdir.endswith("/www"):
                webdir = webdir + "/static"
            else:
                webdir = webdir + "/www/static"
            WEB_DIR = webdir
        self.webdir = WEB_DIR

    def run_in_background(self):
        self.web_server_running = True
        if not self.thread:
            self.thread = threading.Thread(target=lambda: self._run())
            self.thread.start()
        return self

    def stop(self):
        loop = self.loop
        if loop:
            loop.stop()

    def _run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.run()

    def run(self):
        try:
            print("Starting server http://%s:%s" % (self.hostName, self.serverPort))
            self.loop = asyncio.get_event_loop()
            self.loop.run_until_complete(start_server(self.hostName, self.serverPort))
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        self.loop.stop()
        self.loop = None
        self.web_server_running = False
        print("Server http://%s:%s stopped." % (self.hostName, self.serverPort))


if __name__ == "__main__":
    server = None
    try:
        server = MidasServer()
        server.run_in_background()
        while server.web_server_running:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(1)

