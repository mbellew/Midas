from app.MidiMap import MidiMap
from app.Event import EVENT_CLOCK, EVENT_MIDI, EVENT_STOP


class Module:
    def handle(self, event):
        pass


class AbstractModule(Module):
    def __init__(self):
        self.ccmap = MidiMap()

    def handle(self, event):
        if event.code == EVENT_CLOCK:
            self.handle_clock(event.obj)

        if event.code == EVENT_STOP:
            self.handle_stop()

        if event.code == EVENT_MIDI:
            msg = event.obj
            if msg.type == 'control_change':
                self.ccmap.dispatch(msg)

            if msg.type == 'note_on' or msg.type == 'note_off':
                self.handle_note(msg)

    def handle_clock(pulse):
        return

    def handle_stop():
        return

    def handle_note(msg):
        return
