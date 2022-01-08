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
        self.app = None
        self.site = None
        self.loop = None
        self.stopped = False
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
        self.new_message_condition = cond = asyncio.Condition()


    async def start_server(self):
        self.app = web.Application()
        self.app.add_routes([
            web.get('/ws', lambda request: self.websocket_handler(request)),
            web.get('/{file}', lambda request: self.http_handler(request)),
            web.get('/', lambda request: self.http_handler(request)),
        ])
        runner = web.AppRunner(self.app)
        await runner.setup()
        self.site = web.TCPSite(runner, self.hostName, self.serverPort)
        await self.site.start()


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


    async def websocket_handler_poll(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                for i in range(0, 5):
                    if msg.data == 'ping' or self.message_changed:
                        break
                    await asyncio.sleep(0.2)
                await ws.send_str(self.message)
                self.message_changed = False
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
        return ws

    # async def websocket_handler_event(self, request):
    #     ws = web.WebSocketResponse()
    #     await ws.prepare(request)
    #     async for msg in ws:
    #         if msg.type == aiohttp.WSMsgType.TEXT:
    #             if msg.data != 'ping' and not self.new_message_event.is_set():
    #                 asyncio.wait(self.new_message_event.wait(), 0.5)
    #             await ws.send_str(self.message)
    #             self.new_message_event.clear()
    #         elif msg.type == aiohttp.WSMsgType.ERROR:
    #             print('ws connection closed with exception %s' % ws.exception())
    #     return ws

    async def websocket_handler_cond(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                text = None
                await self.new_message_condition.acquire()
                try:
                    while msg.data != 'ping' and not self.message_changed:
                        await asyncio.wait_for(self.new_message_condition.wait(), timeout=1.0)
                    text = self.message
                finally:
                    self.new_message_condition.release()
                await ws.send_str(text)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
        return ws


    async def websocket_handler(self, request):
        return await self.websocket_handler_cond(request)


    def run_in_background(self):
        if not self.thread:
            self.thread = threading.Thread(target=lambda: self.run())
            self.thread.start()
        return self


    async def _stop(self):
        self.stopped = True
        if self.site:
            await self.site.stop()
        if self.app:
            await self.app.cleanup()


    def stop(self):
        asyncio.run(self._stop())


    def run(self):
        try:
            try:
                asyncio.get_event_loop()
            except RuntimeError as re:
                asyncio.set_event_loop(asyncio.new_event_loop())
            print("Starting server http://%s:%s" % (self.hostName, self.serverPort))
            self.loop = asyncio.get_event_loop()
            self.loop.run_until_complete(self.start_server())
            self.loop.run_forever()
        finally:
            self.stopped = True
        self.stop()
        print("Server http://%s:%s stopped." % (self.hostName, self.serverPort))


    async def update(self, message):
        await self.new_message_condition.acquire()
        try:
            if self.message != message:
                self.message = message
                self.message_changed = True
                self.new_message_condition.notify_all()
        finally:
            self.new_message_condition.release()



if __name__ == "__main__":
    import signal
    server = None
    try:
        server = MidasServer()
        server.run_in_background()
        signal.signal(signal.SIGINT, lambda sig, frame: server.stop())
        signal.signal(signal.SIGTERM, lambda sig, frame: server.stop())
        signal.signal(signal.SIGUSR1, lambda sig, frame: server.stop())
        while not server.stopped:
            time.sleep(1)
    finally:
        print("finally")

