from midi.Event import Event, EVENT_MIDI


class TransposeModule:
    def __init__(self, q, midi_cc, midi_in, midi_out):
        self.queue = q
        q.createSink(midi_cc, self)
        q.createSink(midi_in, self)
        self.midi_out = q.createSource(midi_out)
        self.transpose = 0
        if midi_in == midi_out:
            raise


    def handle(self, event):
        if EVENT_MIDI != event.code:
            return
        source = event.source
        msg = event.obj
        if msg.type == 'control_change':
            self.transpose = int((msg.value / 128.0) * 12)
            return
        # TODO make sure note_off is matched to the transposition of the previous note_on!
        if msg.type == 'note_on' or msg.type == 'note_off':
            self.midi_out.add(Event(EVENT_MIDI, source + "/" + self.midi_out.name, msg.copy(note=msg.note+self.transpose)))
        else:
            self.midi_out.add(Event(EVENT_MIDI, source + "/" + self.midi_out.name, msg))
