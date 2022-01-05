from app.MidiMap import MidiMap
from app.Event import EVENT_CLOCK, EVENT_MIDI, EVENT_STOP
from app.DisplayArea import DisplayArea


class Module:
    def handle(self, event):
        pass


class AbstractModule(Module):
    def __init__(self):
        self.display_area = DisplayArea.screen(0,0) # allocate a do-nothing display
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


class ProgramModule(AbstractModule):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.display_area = DisplayArea.screen(0,0)

    def set_display_area(self, d):
        self.display_area = d

    def update_display(self):
        raise Exception("please implement this")

    def get_display_name(self):
        return self.name
        
    def isProgramModule(self):
        return True

    def get_control_sink(type):
        raise Exception("please implement this")


    