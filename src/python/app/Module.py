from app.MidiMap import MidiMap
from app.Event import EVENT_CLOCK, EVENT_MIDI, EVENT_STOP


class Module:
    def handle(self, event):
        pass


class AbstractModule(Module):
    def __init__(self):
        self.ccmap = MidiMap()
        self.time = -1

    def handle(self, event):
        if event.code == EVENT_CLOCK:
            self.time = event.obj.time
            self.handle_clock(event.obj)
        elif event.code == EVENT_MIDI:
            self.handle_midi(event.obj)
        elif event.code == EVENT_STOP:
            self.handle_stop()
            self.time = -1

    def handle_midi(self, msg):
        if msg.type == 'control_change':
            self.handle_cc(msg)
        elif msg.type == 'note_on' or msg.type == 'note_off':
            self.handle_note(msg)

    def handle_cc(self,msg):
        self.ccmap.dispatch(msg)

    def handle_clock(self,pulse):
        return

    def handle_stop(self):
        return

    def handle_note(self,msg):
        return
