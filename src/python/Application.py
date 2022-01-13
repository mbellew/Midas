import asyncio
import signal

from midi.GlobalState import GlobalState
from midi.MidiServer import MidiServer
from www.HttpServer import HttpServer


class Application:
    @staticmethod
    def create():
        if not GlobalState.midiserver:
            GlobalState.midiserver = MidiServer()
        return GlobalState.midiserver


    @staticmethod
    def stop():
        print("Application.py settings stop_event")
        GlobalState.stop_event.set()
        if GlobalState.midiserver_task:
            GlobalState.midiserver_task.cancel()
        if GlobalState.webserver_task:
            GlobalState.webserver_task.cancel()


    @staticmethod
    def sig_int(sig, frame):
        Application.stop()


    @staticmethod
    def sig_term(sig, frame):
        Application.stop()


    @staticmethod
    async def async_run():
        # try:
        #     GlobalState.webserver_task = asyncio.create_task(GlobalState.webserver.async_run())
        #     GlobalState.midiserver_task = asyncio.create_task(GlobalState.midiserver.loop_forever())
        #     await asyncio.wait_for(GlobalState.midiserver_task)
        #     await asyncio.wait_for(GlobalState.webserver_task)
        # finally:
        #     print("async_run setting stop_event")
        #     GlobalState.stop_event.set()
        try:
            GlobalState.webserver_task = asyncio.create_task(GlobalState.webserver.async_run())
            GlobalState.midiserver_task = asyncio.create_task(GlobalState.midiserver.loop_forever())
            while not GlobalState.stop_event.is_set():
                await asyncio.sleep(0.1)
        finally:
            print("async_run setting stop_event")
            GlobalState.stop_event.set()



    @staticmethod
    def run():
        try:
            signal.signal(signal.SIGINT, Application.sig_int)
            signal.signal(signal.SIGTERM, Application.sig_term)

            if not GlobalState.midiserver:
                GlobalState.midiserver = MidiServer()
            if not GlobalState.webserver:
                GlobalState.webserver = HttpServer()
            asyncio.run(Application.async_run())
        finally:
            Application.stop()
            print("finally")
            exit(0)
