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

import mido
from random import random, randrange
from app.MidiMap import MidiMap
from app.Event import Event, EVENT_CLOCK, EVENT_MIDI, EVENT_STOP
from app.Module import AbstractModule
from app.Chords import *



class Carpeggio(AbstractModule):
    def __init__(self, q, clock_sink, cc_sink, notes_out, channel=9, drone=None, ppq=48, root=36):
        super().__init__()
        self.time = -1
        self.root = root
        self.drone_channel = drone
        self.note_prob = 0.92

        self.update_chord(0)
        self.step = -1

        q.createSink(clock_sink,self)
        q.createSink(cc_sink,self)
        self.ppq = ppq
        self.notes_out = q.createSource(notes_out)
        self.channel = channel
        self.notes_currently_on = []
        self.drone_notes = []

    def update_chord(self, measure):
        chord = self.next_chord(measure).copy(transpose=self.root)
        self.arp_chord = chord.chord_shape
        self.chord_offset = chord.root
        self.current_sequence = chord.generate_sequence()

    def next_step(self, pulse):
        return (self.step + 1) % 16

    def next_chord(measure):
        return MAJOR_KEY_CHORDS[randrange(len(MAJOR_KEY_CHORDS))]

    def handle_clock(self, pulse):

        trigger = self.trigger(pulse)

        if not trigger and not pulse.quarter:
            return

        # drone
        if self.drone_channel is not None and pulse.measure:
            if pulse.measure_num % 4 == 0:
                self.update_chord(pulse.measure)
            if pulse.measure_num % 4 == 0:
                current_notes_on = self.drone_notes
                self.drone_notes = []
                off_on = True
                if off_on:
                    for off_msg in current_notes_on:
                        off_msg.time = self.time
                        self.notes_out.add(Event(EVENT_MIDI,'carpeggio.drone',off_msg))
                note = self.current_sequence[0]
                on_msg = mido.Message('note_on', note=note, channel=self.drone_channel, time=self.time)
                off_msg = mido.Message('note_off', note=note, channel=self.drone_channel)
                self.drone_notes.append(off_msg)
                self.notes_out.add(Event(EVENT_MIDI,'carpeggio.drone',on_msg))
                if not off_on:
                    for off_msg in current_notes_on:
                        off_msg.time = self.time
                        self.notes_out.add(Event(EVENT_MIDI,'carpeggio.drone',off_msg))
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
            self.notes_out.add(Event(EVENT_MIDI,'carpeggio.drone',off_msg))
        for i in range(0,16):
            note = self.current_sequence[i]
            off_msg = mido.Message('note_off', note=note, channel=self.channel, time=self.time)
            self.notes_out.add(Event(EVENT_MIDI,'carpeggio',off_msg))


class CarpeggioRand(Carpeggio):
    def __init__(self, q, clock_sink, cc_sink, notes_out, channel=9, ppq=48):
        super().__init__(q, clock_sink, cc_sink, notes_out, channel, ppq)


def rotate_word_right(w, n):
    n = n % 16
    r = ((w & 0x0000ffff) >> n) | ((w << (16-n)) & 0x0000ffff)
    return r

def start_of_bar(pulse):
    return pulse.measure and pulse.measure_num % 4 == 0

class CarpeggioGenerative(Carpeggio):
    def __init__(self, q, clock_sink, cc_sink, notes_out, drone=None, root=36, channel=9, ppq=24, minor=False):
        self.last_chord = -1
        self.minor = minor
        super().__init__(q, clock_sink, cc_sink, notes_out, drone=drone, root=root, channel=channel, ppq=ppq)
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
            # 'restart' sequene
            self.register_rotation = self.register_rotation % 16
            self.register = rotate_word_right(self.register, 16-self.register_rotation)
            self.register_rotation = 0

        #print(hex(self.state))
        curr = self.register
        self.register = rotate_word_right(self.register, 5)
        self.register_rotation = self.register_rotation + 5
        if random() < self.seq_prob:
            self.register = self.register ^ 0x0001
        # This only uses the 8 notes of the 16 available, sounds better to me
        return curr & 0x0007

    def next_chord(self, measure):
        r = random()
        if measure==0:
            c=0
        elif r < 0.2:
            c = 0       # I
        elif r < 0.4:
            c = 4       # V
        elif r < 0.6:
            c = 3       # IV
        elif r < 0.7:
            c = 1       #II
        elif r < 0.8:
            c = 2       #III
        elif r < 0.9:
            c = 5       #VI
        else:
            c = 6       #VII
        if c == self.last_chord:
            c = randrange(0,7)
        print("CHORD " + str(c+1))
        if self.minor:
            return MINOR_KEY_CHORDS[c]
        else:
            return MAJOR_KEY_CHORDS[c]
