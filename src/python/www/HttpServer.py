import threading
import time
import os
import aiohttp
from aiohttp import web
from aiohttp.web_runner import GracefulExit
import asyncio

from midi.GlobalState import GlobalState


class HttpServer:
    def __init__(self, hostName="localhost", serverPort=8080):
        self.hostName = hostName
        self.serverPort = serverPort
        self.thread = None
        self.task = None
        self.app = None
        self.runner = None
        self.site = None
        self.loop = None
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
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, self.hostName, self.serverPort)
        await self.site.start()


    async def http_handler(self, request):
        if GlobalState.stop_event.is_set():
            raise GracefulExit()
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
            if GlobalState.stop_event.is_set():
                raise GracefulExit()
            if msg.type == aiohttp.WSMsgType.TEXT:
                await self.new_message_condition.acquire()
                try:
                    while msg.data != 'ping' and not self.message_changed:
                        try:
                            await asyncio.wait_for(self.new_message_condition.wait(), timeout=1.0)
                        except TimeoutError as te:
                            pass
                    text = self.message
                finally:
                    self.new_message_condition.release()
                await ws.send_str(text)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
        return ws


    async def websocket_handler(self, request):
        return await self.websocket_handler_cond(request)


    def run_in_background(self, loop):
        if not self.thread:
            self.loop = loop
            self.thread = threading.Thread(target=lambda: self.run())
            self.thread.start()
        return self

    async def async_stop(self):
        print("HttpServer.py async_stop")
        GlobalState.stop_event.set()
        if self.site:
            await self.site.stop()
        if self.runner:
            await self.runner.shutdown()
        if self.app:
            await self.app.shutdown()

    def stop(self):
        asyncio.run(self.async_stop())

    async def async_run(self):
        await self.start_server()

    def run(self):
        try:
            try:
                if self.loop:
                    asyncio.set_event_loop(self.loop)
                else:
                    self.loop = asyncio.get_event_loop()
            except RuntimeError as re:
                asyncio.set_event_loop(asyncio.new_event_loop())
            self.loop = asyncio.get_event_loop()
            print("Starting server http://%s:%s" % (self.hostName, self.serverPort))
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


# ## testing
#
#
# def main_stop(server):
#     GlobalState.stop_event.set()
#     asyncio.run(server.async_stop())
#
#
# async def main_start(server):
#     # asyncio.create_task(server.start_server())
#     asyncio.get_event_loop().run_until_complete(server.start_server())


if __name__ == "__main__":
    import signal
    server = MidasServer()
    signal.signal(signal.SIGINT, lambda sig, frame: server.stop())
    signal.signal(signal.SIGTERM, lambda sig, frame: server.stop())
    signal.signal(signal.SIGUSR1, lambda sig, frame: server.stop())
    try:
        server.run_in_background()
        while not GlobalState.stop_event.is_set():
            time.sleep(1)
    finally:
        print("finally")

