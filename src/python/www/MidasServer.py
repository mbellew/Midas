import threading
import time
import os
import aiohttp
from aiohttp import web
import asyncio


class MidasServer:
    def __init__(self, hostName="localhost", serverPort=8080):
        self.hostName = hostName
        self.serverPort = serverPort
        self.thread = None
        self.loop = None
        self.web_server_running = False
        webdir = os.getcwd()
        if webdir.endswith("/static"):
            pass
        elif webdir.endswith("/www"):
            webdir = webdir + "/static"
        else:
            webdir = webdir + "/www/static"
        self.webdir = webdir
        self.message = ' pong '
        # BUGBUG learn how asyncio signalling works!
        self.message_changed = False
        self.new_message_event = asyncio.Event()


    async def start_server(self):
        app = web.Application()
        app.add_routes([
            web.get('/ws', lambda request: self.websocket_handler(request)),
            web.get('/{file}', lambda request: self.http_handler(request)),
            web.get('/', lambda request: self.http_handler(request)),
        ])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.hostName, self.serverPort)
        await site.start()


    async def http_handler(self, request):
        request_path = request.url.path
        if request_path == '/':
            request_path = '/index.html'
        elif -1 != request_path.find(".."):
            raise web.HTTPNotFound()
        elif -1 != request_path.find("/", 1):
            raise web.HTTPNotFound()
        os_path = self.webdir + request_path
        if os.path.exists(os_path):
            return web.FileResponse(os_path)


    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    for i in range(0,5):
                        if msg.data == 'ping' or self.message_changed:
                            break
                        await asyncio.sleep(0.1)
                    await ws.send_str(self.message)
                    self.message_changed = False
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
        return ws


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
            self.loop.run_until_complete(self.start_server())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        self.loop.stop()
        self.loop = None
        self.web_server_running = False
        print("Server http://%s:%s stopped." % (self.hostName, self.serverPort))


    def update(self, message):
        self.message = message
        self.new_message_event.set()
        self.message_changed = True


if __name__ == "__main__":
    server = None
    try:
        server = MidasServer()
        server.run_in_background()
        while server.web_server_running:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(1)

