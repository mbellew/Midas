from Event import EVENT_MIDI, EVENT_CONTINUE, EVENT_DONE, EVENT_MEASURE
import mido

from PatchQueue import SINK_POINT
#from math import max, min


class StrumPattern:
    def __init__(self, q, sinkName, sourceName):
        q.createSink(sinkName, self)
        self.out = q.createSource(sourceName)
        self.current_msg = None
        self.source = None


    def handle(self, event):

        if event[0] == EVENT_MIDI:
            self.source = event[1]
            msg = event[2]
            if msg.type == 'note_on':
                self.current_msg = msg
            if msg.type == 'note_off':
                if self.current_msg and self.current_msg.note == msg.note:
                    self.current_msg = None
            return EVENT_DONE
        
        if event[0] == EVENT_MEASURE:
            if not self.current_msg or self.current_msg.type != 'note_on':
                return EVENT_CONTINUE            
            msg = self.current_msg
            # send a measure worth of notes
            msg_down = msg.copy(velocity=max(msg.note+20,127))
            msg_up   = msg.copy(velocity=min(msg.note-20,10))
            self.out.delay((EVENT_MIDI, self.source + '/' + self.out.name, msg_down), 0)  # D
            self.out.delay((EVENT_MIDI, self.source + '/' + self.out.name, msg_down), 24) # D
            self.out.delay((EVENT_MIDI, self.source + '/' + self.out.name, msg_up), 36) # U
            self.out.delay((EVENT_MIDI, self.source + '/' + self.out.name, msg_up), 60) # U
            self.out.delay((EVENT_MIDI, self.source + '/' + self.out.name, msg_down), 72) # D
            self.out.delay((EVENT_MIDI, self.source + '/' + self.out.name, msg_up), 84) # U
            off = mido.Message('note_off', note=msg.note)
            self.out.delay((EVENT_MIDI, self.source + '/' + self.out.name, off), 94) # U
        
        return EVENT_CONTINUE 
