from Event import EVENT_MIDI, EVENT_CONTINUE, EVENT_DONE, EVENT_MEASURE, EVENT_TEMPO
import mido


class StrumArpeggiator:
    def __init__(self, q, sinkName, sourceName, minor=False):
        q.createSink(sinkName,self)
        self.out = q.createSource(sourceName)
        self.minor = minor
        self.pulse = 0
        self.last_note_strummed = 0
        self.notes_off = []

    def handle(self, event):

        if event[0] == EVENT_TEMPO:
            self.pulse = event[1]
            return EVENT_CONTINUE

        if event[0] != EVENT_MIDI:
            return EVENT_CONTINUE

        source = event[1]
        msg = event[2]
        
        if msg.type == 'note_on' or msg.type == 'note_off':
            if msg.type == 'note_on' or (msg.type == 'note_off' and msg.note == self.last_note_strummed):
                self.out.remove_all(lambda e : e[0] == EVENT_MIDI and e[2].type == 'note_on')
                for m in self.notes_off:
                    self.out.delay((EVENT_MIDI, source + '/' + self.out.name, m), 9)
                self.notes_off = []
            if msg.type == 'note_on':
                speed = 3
                self.last_note_strummed = msg.note
                notes_on = [
                    msg.copy(note=msg.note+0),
                    msg.copy(note=msg.note+(3 if self.minor else 4)),
                    msg.copy(note=msg.note+7),
                    msg.copy(note=msg.note+12)
                ]
                for n in notes_on :
                    self.notes_off.append(mido.Message('note_off', note=n.note))
                # find place in measure
                if self.pulse % 24 < 12:
                    self.out.delay((EVENT_MIDI, source + '/' + self.out.name, notes_on[0]), 0*speed)
                    self.out.delay((EVENT_MIDI, source + '/' + self.out.name, notes_on[1]), 1*speed)
                    self.out.delay((EVENT_MIDI, source + '/' + self.out.name, notes_on[2]), 2*speed)
                    self.out.delay((EVENT_MIDI, source + '/' + self.out.name, notes_on[3]), 3*speed)
                else:
                    self.out.delay((EVENT_MIDI, source + '/' + self.out.name, notes_on[3]), 0*speed)
                    self.out.delay((EVENT_MIDI, source + '/' + self.out.name, notes_on[2]), 1*speed)
                    self.out.delay((EVENT_MIDI, source + '/' + self.out.name, notes_on[1]), 2*speed)
                    self.out.delay((EVENT_MIDI, source + '/' + self.out.name, notes_on[0]), 3*speed)
        else:
            self.out.add((EVENT_MIDI, source + '/' + self.out.name, msg))
        return
