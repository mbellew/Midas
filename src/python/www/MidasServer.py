import threading
import time
import os
import aiohttp
from aiohttp import web
import asyncio

# TODO pass this to http_handler() somehow, instead of having global
# TODO learn signals/events in asyncio
WEB_DIR = None
MESSAGE = ' pong '
# BUGBUG
message_changed = False
new_message_event = asyncio.Event()


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
    global MESSAGE, new_message_event, message_changed
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                for i in range(0,5):
                    if msg.data == 'ping' or message_changed:
                        break
                    await asyncio.sleep(0.1)
                await ws.send_str(MESSAGE)
                message_changed = False
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


    def update(self, message):
        global MESSAGE, new_message_event, message_changed
        MESSAGE = message
        new_message_event.set()
        message_changed = True


if __name__ == "__main__":
    server = None
    try:
        server = MidasServer()
        server.run_in_background()
        while server.web_server_running:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(1)

