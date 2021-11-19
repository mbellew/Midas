from typing import SupportsRound
from Event import EVENT_MIDI, EVENT_CONTINUE, EVENT_DONE


class TransposeModule:
    def __init__(self, q, midi_cc, midi_in, midi_out):
        self.queue = q
        q.createSink(midi_cc,self)
        q.createSink(midi_in, self)
        self.midi_out = q.createSource(midi_out)
        self.transpose = 0
        if midi_in == midi_out:
            raise


    def handle(self, event):
        if event[0] != EVENT_MIDI:
            return EVENT_CONTINUE
        source = event[1]
        msg = event[2]
        if event[1] == self.midi_cc and msg.type == 'control_change':
            self.transpose = int((msg.value / 128.0) * 12)
            return EVENT_DONE
        if event[1] == self.midi_in:
            # TODO make sure note_off is matched to the transposition of the previous note_on!
            if msg.type == 'note_on' or msg.type == 'note_off':
                self.queue.add((EVENT_MIDI, source + "/" + self.midi_out.name, msg.copy(note=msg.note+self.transpose)))
            else:
                self.queue.add((EVENT_MIDI, source + "/" + self.midi_out.name, msg))
            return EVENT_DONE
        return EVENT_CONTINUE
