import mido
from random import random, randrange
from app.MidiMap import MidiMap
from app.Event import Event, EVENT_CLOCK, EVENT_MIDI, EVENT_STOP
from app.Module import AbstractModule


# adapted from https://github.com/Chysn/O_C-HemisphereSuite/wiki/Carpeggio-Cartesian-Arpeggiator

class ArpChord:
    def __init__(self, name, tones, nr_notes, octave_span):
        self.chord_name = name
        self.chord_tones = tones
        self.nr_notes = nr_notes
        self.octave_span = octave_span

    def generate_sequence(self, root):
        octaves = 2
        sequence = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for s in range(0,16):
            oct = int(s / self.nr_notes) % octaves
            tone = int(s % self.nr_notes)
            sequence[s] = int(self.chord_tones[tone] + (12 * oct) + root)
        return sequence


arp_chords = [
  #ARPEGGIATE
  ArpChord("Maj triad",[0, 4, 7], 3,1),
  ArpChord("Maj inv 1",[4, 7, 12], 3,1),
  ArpChord("Maj inv 2",[7, 12, 16], 3,1),
  ArpChord("min triad",[0, 3, 7], 3,1),
  ArpChord("min inv 1",[3, 7, 12], 3,1),
  ArpChord("min inv 2",[7, 12, 15], 3,1),
  ArpChord("dim triad",[0, 3, 6],3,1),
  ArpChord("Octaves",[0],1,1),
  ArpChord("1 5",[0, 7],2,1),

  ArpChord("aug triad",[0, 4, 8],3,1),
  ArpChord("sus2",[0,2,7],3,1),
  ArpChord("sus4",[0,5,7],3,1),
  ArpChord("add2",[0,2,4,7],4,1),
  ArpChord("min(add2)",[0,2,3,7],4,1),

  ArpChord("add4",[0,4,5,7],4,1),
  ArpChord("min(+4)",[0,3,5,7],4,1),
  ArpChord("sus4(+2)",[0,2,6,7],4,1),
  ArpChord("12345",[0,2,4,5,7],5,1),
  ArpChord("12b345",[0,2,3,5,7],5,1),

  ArpChord("add(#11)",[0,4,6,7],4,1),
  ArpChord("Maj6",[0,4,7,9],4,1),
  ArpChord("min6",[0,3,7,9],4,1),
  ArpChord("Maj7",[0,4,7,11],4,1),
  ArpChord("7",[0,4,7,10],4,1),
  #////////     20     /////
  ArpChord("7sus2",[0,2,7,10],4,1),
  ArpChord("7sus4",[0,5,7,10],4,1),
  ArpChord("min7",[0,3,7,10],4,1),
  ArpChord("dim7",[0,3,6,8],4,1),
  ArpChord("Maj9",[0,4,7,11,14],5,1),

  ArpChord("Maj6/9",[0,4,7,9,14],5,1),
  ArpChord("Maj#11",[0,4,7,11,14,18],6,2),
  ArpChord("9",[0,4,7,10,14],5,1),
  ArpChord("7(b9)",[0,4,7,10,13],5,1),
  ArpChord("7(b9,b13)",[0,4,7,10,13,20],6,2),
  #////////     30     /////
  ArpChord("Ionian",[0,2,4,5,7,9,11],7,1),
  ArpChord("Dorian",[0,2,3,5,7,9,10],7,1),
  ArpChord("Phrygian",[0,1,3,5,7,8,10],7,1),
  ArpChord("Lydian",[0,2,4,6,7,9,11],7,1),
  ArpChord("Mixolyd.",[0,2,4,5,7,9,10],7,1),

  ArpChord("Aeolian",[0,2,3,5,7,8,10],7,1),
  ArpChord("Locrian",[0,1,3,5,6,8,10],7,1),
  ArpChord("Harm Min",[0,2,3,5,7,8,11],7,1),
  ArpChord("Mel Min",[0,2,3,5,7,9,11],7,1),
  ArpChord("Penta",[0,2,4,7,9],5,1),
  #//////////    40 ////////
  ArpChord("min Penta",[0,3,5,7,10],5,1),
  ArpChord("Maj Blues",[0,2,3,4,7,9],6,1),
  ArpChord("min Blues",[0,3,5,6,7,10],6,1),
  ArpChord("Bebop",[0,2,4,5,7,9,10,11],8,1),
  ArpChord("WholeTone",[0,2,4,6,8,10],6,1),

  ArpChord("Dim 1 1/2",[0,2,3,5,6,8,9,11],8,1),
  ArpChord("Dim 1/2 1",[0,2,3,5,6,8,9,11],8,1),
  ArpChord("Altered",[0,1,3,4,6,8,10],7,1),
  ArpChord("Chromatic",[0,1,2,3,4,5,6,7,8,9,10,11],12,1),
  ArpChord("All 4th",[0,5,10,15,20,26,31],7,3),
  #//////////    50 ////////
  ArpChord("All 5th",[0,7,14,21,28,35,41],7,4)
]

def find_chord(chord_desc):
    chord = None
    if type(chord_desc) == type(""):
        for c in arp_chords:
            if c.chord_name == chord_desc:
                chord = c
                break
    else:
        chord = arp_chords[chord_desc % len(arp_chords)]
    if chord is None:
        raise("chord not found: " + chord_desc)
    return chord


# returns int[16] of midi notes
def generate_sequence(chord_desc,root=36):
    chord = find_chord(chord_desc)
    return chord.generate_sequence(root)


MAJOR_KEY_CHORDS = [
    (find_chord("Maj triad"),0),  #C   I
    (find_chord("min triad"),2),  #D   ii
    (find_chord("min triad"),4),  #E   iii
    (find_chord("Maj triad"),5),  #F   IV
    (find_chord("Maj triad"),7),  #G   V
    (find_chord("min triad"),-3),  #A   vi
    (find_chord("dim triad"),-1)  #B   viio Diminished triad
]
MINOR_KEY_CHORDS = [
    (find_chord("min triad"),0),  #C   i
    (find_chord("dim triad"),2),  #D   iio Diminished triad
    (find_chord("aug triad"),4),  #E   III+ Augmented triad
    (find_chord("min triad"),5),  #F   iv
    (find_chord("Maj triad"),7),  #G   V
    (find_chord("Maj triad"),-3),  #A   VI
    (find_chord("dim triad"),-1)  #B   viio Diminished triad
]


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
        pair = self.next_chord(measure)
        self.arp_chord = pair[0]
        self.chord_offset = pair[1]
        self.current_sequence = self.arp_chord.generate_sequence(self.root + self.chord_offset)

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
    def __init__(self, q, clock_sink, cc_sink, notes_out, drone=None, channel=9, ppq=24, minor=False):
        self.last_chord = -1
        self.minor = minor
        super().__init__(q, clock_sink, cc_sink, notes_out, drone=drone, channel=channel, ppq=ppq)
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
