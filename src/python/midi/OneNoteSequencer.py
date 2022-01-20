
from random import random, randrange

import mido

from midi.Event import Event, EVENT_MIDI
from midi.Module import ProgramModule
from midi.Sequencer import Sequencer
from midi.GlobalState import GlobalState


class OneNoteSequencer(Sequencer):
    def __init__(self, q, name, note=36, minor=False):
        super().__init__(q,name)
        self.note = note
        q.createSink(name + "_note_in", self.handle_note_in)

    def handle_note_in(self, event):
        if event.code == EVENT_MIDI and event.obj.type == 'note_on' and event.obj.velocity > 0:
            self.note = event.obj.note

    def play_notes(self):
        return [(mido.Message('note_on',note=self.note), 1)]
