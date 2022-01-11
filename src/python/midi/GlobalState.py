import threading

class _GlobalState:
    def __init__(self):
        self.stop_event = threading.Event()
        self.webserver = None
        self.webserver_task = None
        self.midiserver = None
        self.midiserver_task = None


GlobalState = _GlobalState()