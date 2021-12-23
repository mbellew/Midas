import mido
from random import random, randrange
from app.MidiMap import MidiMap
from app.Event import Event, EVENT_CLOCK, EVENT_MIDI

# adapted from https://github.com/Chysn/O_C-HemisphereSuite/wiki/Carpeggio-Cartesian-Arpeggiator

class ArpChord:
    def __init__(self, name, tones, nr_notes, octave_span):
        self.chord_name = name
        self.chord_tones = tones
        self.nr_notes = nr_notes
        self.octave_span = octave_span

    def generate_sequence(self, root):
        sequence = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for s in range(0,16):
            oct = (s / self.nr_notes) % 3
            tone = s % self.nr_notes
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
            generate_sequence("Maj triad",0),  #C   I
            generate_sequence("min triad",2),  #D   ii
            generate_sequence("min triad",4),  #E   iii
            generate_sequence("Maj triad",5),  #F   IV
            generate_sequence("Maj triad",7),  #G   V
            generate_sequence("min triad",9),  #A   vi
            generate_sequence("dim triad",11)  #B   viio Diminished triad
]
MINOR_KEY_CHORDS = [
            generate_sequence("min triad",0),  #C   i
            generate_sequence("dim triad",2),  #D   iio Diminished triad
            generate_sequence("aug triad",4),  #E   III+ Augmented triad
            generate_sequence("min triad",5),  #F   iv
            generate_sequence("Maj triad",7),  #G   V
            generate_sequence("Maj triad",9),  #A   VI
            generate_sequence("dim triad",11)  #B   viio Diminished triad
]

class Carpeggio:
    def __init__(self, q, clock_sink, cc_sink, notes_out, channel=9, drone=None, ppq=48):
        self.root = 36
        self.drone = drone
        self.note_prob = 0.95

        # step sequencer and chord sequencer functions
        self.next_step_fn = lambda step : (step + 1) % 16
        self.next_chord_fn = lambda measure : MAJOR_KEY_CHORDS[randrange(len(MAJOR_KEY_CHORDS))]

        self.current_sequence = self.next_chord_fn(0)
        self.step = -1

        q.createSink(clock_sink,self)
        q.createSink(cc_sink,self)
        self.ppq = ppq
        self.notes_out = q.createSource(notes_out)
        self.channel = channel
        self.notes_currently_on = []
        self.drone_notes = []
        self.ccmap = MidiMap()

    def handle(self, event):
        if event.code == EVENT_CLOCK:
            pulse = event.obj
            if pulse.pulse != 0:
                return

            # drone
            if self.drone is not None and pulse.beat == 0:
                if pulse.measure%4 == 0:
                    for off_msg in self.drone_notes:
                        self.notes_out.add(Event(EVENT_MIDI,'carpeggio.drone',off_msg))
                    self.drone_notes = []
                    self.current_sequence = self.next_chord_fn(pulse.measure)
                    note = self.root + self.current_sequence[0]
                    on_msg = mido.Message('note_on', note=note, channel=self.drone)
                    off_msg = mido.Message('note_off', note=note, channel=self.drone)
                    self.drone_notes.append(off_msg)
                    self.notes_out.add(Event(EVENT_MIDI,'carpeggio.drone',on_msg))
                elif pulse.measure%4 == 2:
                    note = self.current_sequence[0]
                    on_msg = mido.Message('note_on', note=note, channel=self.drone)
                    self.notes_out.add(Event(EVENT_MIDI,'carpeggio.drone',on_msg))

            # bass motif
            for off_msg in self.notes_currently_on:
                self.notes_out.add(Event(EVENT_MIDI,'carpeggio',off_msg))
            self.notes_currently_on = []
            self.step = self.next_step_fn(self.step)
            if random() < self.note_prob:
                note = self.root + self.current_sequence[self.step % 16]
                on_msg = mido.Message('note_on', note=note, channel=self.channel)
                off_msg = mido.Message('note_off', note=note, channel=self.channel)
                self.notes_currently_on.append(off_msg)
                self.notes_out.add(Event(EVENT_MIDI,'carpeggio',on_msg))
        if event.code == EVENT_MIDI:
            msg = event.obj
            if msg.type == 'control_change':
                self.ccmap.dispatch(msg)


class CarpeggioRand(Carpeggio):
    def __init__(self, q, clock_sink, cc_sink, notes_out, channel=9, ppq=48):
        super().__init__(q, clock_sink, cc_sink, notes_out, channel, ppq)
        self.next_step_fn = lambda step : int(random() * 0xffffffff)


class CarpeggioGenerative(Carpeggio):
    def __init__(self, q, clock_sink, cc_sink, notes_out, drone=None, channel=9, ppq=48, minor=False):
        super().__init__(q, clock_sink, cc_sink, notes_out, drone=drone, channel=channel, ppq=ppq)
        self.minor = minor
        self.seq_prob = 0.05
        self.state = int(random() * 210343859341) & 0xffff
        self.last_chord = -1
        self.next_step_fn  = lambda step : self.next_step()
        self.next_chord_fn = lambda measure : self.next_chord()

    def next_step(self):
        print(hex(self.state))
        curr = self.state & 0x000f
        s = (self.state << 5) | ((self.state >> 11) & 0x001f)
        if random() < self.seq_prob:
            s = s ^ 0x0001
        self.state = s & 0x0000ffff
        return curr

    def next_chord(self):
        r = random()
        if r < 0.2:
            c = 0
        elif r < 0.4:
            c = 1
        elif r < 0.6:
            c = 2
        elif r < 0.7:
            c = 3
        elif r < 0.8:
            c = 4
        elif r < 0.9:
            c = 5
        else:
            c = 6
        if c != self.last_chord:
            self.last_chord = c
        else:
            self.last_chord = randrange(0,7)
        if self.minor:
            return MINOR_KEY_CHORDS[self.last_chord]
        else:
            return MAJOR_KEY_CHORDS[self.last_chord]
