
from random import random, randrange

import mido

from midi.Event import Event, EVENT_MIDI
from midi.Module import ProgramModule
from midi.Sequencer import Sequencer
from midi.GlobalState import GlobalState


class OneNoteSequencer(Sequencer):
    def __init__(self, q, name, transpose=0, note=36):
        super().__init__(q,name)
        self.note = note
        self.transpose = 0
        q.createSink(name + "_note_in", self.handle_note_in)

    def handle_note_in(self, event):
        if event.code == EVENT_MIDI and event.obj.type == 'note_on' and event.obj.velocity > 0:
            n = event.obj.note + self.transpose
            if n < 0:
                n  = 0
            elif n > 127:
                n = 127
            self.note = n

    def play_notes(self):
        return [(mido.Message('note_on',note=self.note), 1)]
