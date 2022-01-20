# adapted from https://github.com/Chysn/O_C-HemisphereSuite/wiki/Carpeggio-Cartesian-Arpeggiator
"""
// Copyright (c) 2018, Jason Justian
//
// Chord library (c) 2018, Roel Das
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
"""

from random import random, randrange

import mido

from midi.Chords import *
from midi.Event import Event, EVENT_MIDI
from midi.Module import ProgramModule
from midi.Sequencer import Sequencer
from midi.GlobalState import GlobalState


def rotate_word_right(w, n):
    n = n % 16
    r = ((w & 0x0000ffff) >> n) | ((w << (16-n)) & 0x0000ffff)
    return r

def start_of_bar(pulse):
    return pulse.measure and pulse.measure_num % 4 == 0

# TODO add drone

# arepegiate using chords within the defined key
# use a euclidean like pattern for choosing notes
# use a random rythym unless we detect external triggers firing

class ChordySequencer(Sequencer):
    def __init__(self, q, name, root=36, minor=False):
        super().__init__(q,name)
        self.root = root
        self.last_chord = -1
        self.minor = minor
        self.chord_offset = self.root
        self.play_next_chord = None
        self.last_chord_change_measure = 0
        q.createSink(name + "_chord_in", self.handle_chord_in)
        self.root_note_source = q.createSource(name + "_root")
        self.seq_prob = 0.05
        self.register = int(random() * 210343859341) & 0xffff
        self.register_rotation = 0

        # generate random triggers for 32 steps
        # euclidian pattern?  evolving pattern?
        self.triggers = [False] * 32
        r = 0
        for i in range(0, randrange(20,24)):
            self.triggers[r%32] = True
            r = r + randrange(4,6)
        self.trigger_step = 0
        self.eighths = int(GlobalState.PPQ/2)


    def handle_chord_in(self, event):
        # set chord at start of next measure
        # we want a number 1-7 from incoming note
        if event.code == EVENT_MIDI:
            msg = event.obj
            if msg.type == 'note_on':
                n = msg.note % 12
                chord = 0
                if n == 0: chord = 0    # I
                elif n <= 2: chord = 1  # II
                elif n <= 4: chord = 2  # III
                elif n <= 5: chord = 3  # IV
                elif n <= 7: chord = 4  # V
                elif n <= 9: chord = 5  # VI
                else: chord = 6         # VII
                self.play_next_chord = chord


    def handle_clock(self, pulse):
        super().handle_clock(pulse)

        # handle chord changes
        if pulse.measure:
            chord = self.next_chord(pulse.measure_num)
            if chord:
                self.set_notes(chord.generate_sequence(16,2))
                self.chord_offset = chord.root
                # TODO should probably send note_off for this even though right now it's not going straint to a midi output
                self.root_note_source.add(Event(EVENT_MIDI, self.name, mido.Message('note_on', note=chord.root)))

        # handle note triggers
        if self.external_trigger_seen:
            return
        if not pulse.eighth:
            return
        if start_of_bar(pulse):
            self.trigger_step = 0
        if self.triggers[self.trigger_step]:
            self.trigger()
        self.trigger_step = self.trigger_step+1


    def play_notes(self):
        pulse = GlobalState.pulse
        # if we have an external trigger, pulse may not be set!??
        if start_of_bar(pulse):
            # 'restart' sequence
            self.register_rotation = self.register_rotation % 16
            self.register = rotate_word_right(self.register, 16-self.register_rotation)
            self.register_rotation = 0

        # print(hex(self.state))
        curr = self.register
        self.register = rotate_word_right(self.register, 5)
        self.register_rotation = self.register_rotation + 5
        if random() < self.seq_prob:
            self.register = self.register ^ 0x0001

        # This only uses the 8 notes of the 16 available, sounds better to me
        n = curr & 0x0007
        note = self.notes[n % len(self.notes)]
        return [(mido.Message('note_on',note=note), 1)]


    def next_chord(self, measure):
        c = None
        if self.play_next_chord is not None:
            c = self.play_next_chord
        elif measure == 0:
            c = 0
        elif measure - self.last_chord_change_measure >= 4:
            r = random()
            if r < 0.2:
                c = 0       # I
            elif r < 0.4:
                c = 4       # V
            elif r < 0.6:
                c = 3       # IV
            elif r < 0.7:
                c = 1       # II
            elif r < 0.8:
                c = 2       # III
            elif r < 0.9:
                c = 5       # VI
            else:
                c = 6       # VII
            if c == self.last_chord:
                c = randrange(0, 7)
        if c is None:
            return None
        self.play_next_chord = None
        self.last_chord_change_measure = measure
        if self.minor:
            return MINOR_KEY_CHORDS[c].copy(self.root)
        else:
            return MAJOR_KEY_CHORDS[c].copy(self.root)


class ChordyModule(ProgramModule):
    def __init__(self, q, name, root=36, minor=False):
        super().__init__(name)
        self.sequencer = ChordySequencer(q, name, root, minor)

    def update_display(self):
        self.display_area.write(0, 0, "root note " + str(self.sequencer.root))
        self.display_area.write(1, 0, "minor" if self.sequencer.minor else "major")
        c = self.sequencer.chord_offset - self.sequencer.root
        self.display_area.write(2, 0, str(c))

