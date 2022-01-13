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


class Carpeggio(ProgramModule):
    def __init__(self, q, name, channel=1, drone=8, ppq=48, root=36):
        super().__init__("Carpeggio")
        self.time = -1
        self.root = root
        self.drone_channel = drone
        self.note_prob = 0.92

        self.arp_chord = None
        self.chord_offset = None
        self.current_sequence = None
        self.update_chord(0)
        self.step = -1

        q.createSink(name + "_clock_in", self)

        self.cc_sink = q.createSink(name + "_cc_in", self)
        self.ppq = ppq
        self.notes_out = q.createSource(name + "_out")
        self.drone_out = q.createSource(name + "_drone")
        self.channel = channel
        self.notes_currently_on = []
        self.drone_notes = []

    def update_display(self):
        self.display_area.write(0, 0, "root note " + str(self.root))

    def get_control_sink(self):
        return self.cc_sink

    def update_chord(self, measure):
        chord = self.next_chord(measure)
        if chord is None:
            return False
        chord = chord.copy(transpose=self.root)
        self.arp_chord = chord.chord_shape
        self.chord_offset = chord.root
        self.current_sequence = chord.generate_sequence()
        return True

    def next_step(self, pulse):
        return (self.step + 1) % 16

    def next_chord(self, measure):
        return MAJOR_KEY_CHORDS[randrange(len(MAJOR_KEY_CHORDS))]

    def handle_clock(self, pulse):

        trigger = self.trigger(pulse)

        if not trigger and not pulse.quarter:
            return

        # drone
        if self.drone_out is not None and pulse.measure:
            if self.update_chord(pulse.measure_num):
                current_notes_on = self.drone_notes
                self.drone_notes = []
                legato = False
                if not legato:
                    for off_msg in current_notes_on:
                        off_msg.time = self.time
                        self.drone_out.add(Event(EVENT_MIDI, 'carpeggio.drone', off_msg))
                note = self.current_sequence[0]
                on_msg = mido.Message('note_on', note=note, channel=self.drone_channel, time=self.time)
                off_msg = mido.Message('note_off', note=note, channel=self.drone_channel)
                self.drone_notes.append(off_msg)
                self.drone_out.add(Event(EVENT_MIDI, 'carpeggio.drone', on_msg))
                if legato:
                    for off_msg in current_notes_on:
                        off_msg.time = self.time
                        self.drone_out.add(Event(EVENT_MIDI, 'carpeggio.drone', off_msg))
                    self.drone_notes = []

        # bass motif
        if trigger or pulse.quarter:
            for off_msg in self.notes_currently_on:
                off_msg.time = self.time
                self.notes_out.add(Event(EVENT_MIDI,'carpeggio',off_msg))
        self.notes_currently_on = []

        if trigger:
            self.step = self.next_step(pulse)
            note = self.current_sequence[self.step % 16]
            on_msg = mido.Message('note_on', note=note, channel=self.channel, time=self.time)
            if random() > self.note_prob:
                on_msg.velocity = 0
            elif pulse.measure:
                on_msg.velocity = min(127,int(on_msg.velocity*1.25))
            off_msg = mido.Message('note_off', note=note, channel=self.channel)
            self.notes_currently_on.append(off_msg)
            self.notes_out.add(Event(EVENT_MIDI,'carpeggio',on_msg))

    # by default play every quarter note
    def trigger(self, pulse):
        return pulse.beat

    def handle_stop(self):
        for off_msg in self.notes_currently_on:
            self.notes_out.add(Event(EVENT_MIDI,'carpeggio',off_msg))
        for off_msg in self.drone_notes:
            self.drone_out.add(Event(EVENT_MIDI,'carpeggio.drone',off_msg))
        for i in range(0,16):
            note = self.current_sequence[i]
            off_msg = mido.Message('note_off', note=note, channel=self.channel, time=self.time)
            self.notes_out.add(Event(EVENT_MIDI,'carpeggio',off_msg))


class CarpeggioRand(Carpeggio):
    def __init__(self, q, name, ppq=24):
        super().__init__(q, name, ppq=ppq)


def rotate_word_right(w, n):
    n = n % 16
    r = ((w & 0x0000ffff) >> n) | ((w << (16-n)) & 0x0000ffff)
    return r

def start_of_bar(pulse):
    return pulse.measure and pulse.measure_num % 4 == 0


class CarpeggioGenerative(Carpeggio):
    def __init__(self, q, name, root=36, ppq=24, minor=False):
        self.last_chord = -1
        self.minor = minor
        self.play_next_chord = None
        self.last_chord_change_measure = 0
        super().__init__(q, name, root=root, ppq=ppq)
        q.createSink(name + "_chord_in", self.set_next_chord)
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
        self.eighths = int(ppq/2)


    def set_next_chord(self, event):
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


    def update_display(self):
        self.display_area.write(0, 0, "root note " + str(self.root))
        self.display_area.write(1, 0, "minor" if self.minor else "major")
        c = self.chord_offset - self.root
        self.display_area.write(2, 0, str(c))


    def trigger(self, pulse):
        if not pulse.eighth:
            return
        if start_of_bar(pulse):
            self.trigger_step = 0
        t = self.triggers[self.trigger_step]
        self.trigger_step = self.trigger_step+1
        return t
 
    def next_step(self, pulse):
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
        return curr & 0x0007

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
            return MINOR_KEY_CHORDS[c]
        else:
            return MAJOR_KEY_CHORDS[c]
