import mido
from midi.Event import Event, EVENT_MIDI, EVENT_CLOCK


class StrumPattern:
    def __init__(self, q, sinkName, sourceName):
        q.createSink(sinkName, self)
        self.out = q.createSource(sourceName)
        self.current_msg = None
        self.source = None


    def handle(self, event):

        if EVENT_MIDI == event.code:
            self.source = event.source
            msg = event.obj
            if msg.type == 'note_on':
                self.current_msg = msg
            if msg.type == 'note_off':
                if self.current_msg and self.current_msg.note == msg.note:
                    self.current_msg = None
            return
        
        if EVENT_CLOCK == event.code and event.obj.beat == 0 and event.obj.pulse == 0:
            if not self.current_msg or self.current_msg.type != 'note_on':
                return
            msg = self.current_msg
            # send a measure worth of notes
            msg_down = msg.copy(velocity=max(msg.note+20,127))
            msg_up   = msg.copy(velocity=min(msg.note-20,10))
            off = mido.Message('note_off', note=msg.note)
            self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, msg_down), 0)  # D
            self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, off), 23) # U
            self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, msg_down), 24) # D
            self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, off), 35) # U
            self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, msg_up), 36) # U
            self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, off), 59) # U
            self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, msg_up), 60) # U
            self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, off), 71) # U
            self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, msg_down), 72) # D
            #self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, msg_up), 84) # U
            self.out.delay(Event(EVENT_MIDI, self.source + '/' + self.out.name, off), 94) # U
        return 
