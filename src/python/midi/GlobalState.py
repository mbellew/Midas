import threading

class _GlobalState:
    def __init__(self):
        self.stop_event = threading.Event()
        print("GlobalState is_set=" + str(self.stop_event.is_set()))
        self.webserver = None
        self.webserver_task = None
        self.midiserver = None
        self.midiserver_task = None
        self.PPQ = 24
        self.pulse = None


GlobalState = _GlobalState()
