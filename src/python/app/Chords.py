# adapted from https://github.com/Chysn/O_C-HemisphereSuite/wiki/Carpeggio-Cartesian-Arpeggiator

class ChordShape:
    def __init__(self, name, tones, octave_span=1):
        self.chord_name = name
        self.chord_tones = tones
        self.nr_notes = len(tones)
        self.octave_span = octave_span

    def generate_sequence(self, root, sequence=16, octaves=2):
        if type(sequence)==int:
            sequence = [0] * sequence
        for s in range(0,len(sequence)):
            oct = int(s / self.nr_notes) % octaves
            tone = int(s % self.nr_notes)
            sequence[s] = int(self.chord_tones[tone] + (12 * oct) + root)
        return sequence


class Chord:
    def __init__(self, chord_shape, root):
        global find_chord
        typ = type(chord_shape)
        if typ == ChordShape:
            pass
        elif typ == Chord:
            chord_shape = chord_shape.chord_shape
        else:
            chord_shape = find_chord(str)
        self.root = root
        self.chord_shape = chord_shape

    def copy(self, transpose=0):
        return Chord(self.chord_shape, self.root+transpose)

    def generate_sequence(self, sequence=16, octaves=2):
        return self.chord_shape.generate_sequence(self.root, sequence, octaves)



CHORD_SHAPES = [
  #ARPEGGIATE
  ChordShape("Maj triad",[0, 4, 7]),
  ChordShape("Maj inv 1",[4, 7, 12]),
  ChordShape("Maj inv 2",[7, 12, 16]),
  ChordShape("min triad",[0, 3, 7]),
  ChordShape("min inv 1",[3, 7, 12]),
  ChordShape("min inv 2",[7, 12, 15]),
  ChordShape("dim triad",[0, 3, 6]),
  ChordShape("Octaves",[0]),
  ChordShape("1 5",[0, 7]),

  ChordShape("aug triad",[0, 4, 8]),
  ChordShape("sus2",[0,2,7]),
  ChordShape("sus4",[0,5,7]),
  ChordShape("add2",[0,2,4,7]),
  ChordShape("min(add2)",[0,2,3,7]),

  ChordShape("add4",[0,4,5,7]),
  ChordShape("min(+4)",[0,3,5,7]),
  ChordShape("sus4(+2)",[0,2,6,7]),
  ChordShape("12345",[0,2,4,5,7]),
  ChordShape("12b345",[0,2,3,5,7]),

  ChordShape("add(#11)",[0,4,6,7]),
  ChordShape("Maj6",[0,4,7,9]),
  ChordShape("min6",[0,3,7,9]),
  ChordShape("Maj7",[0,4,7,11]),
  ChordShape("7",[0,4,7,10]),
  #////////     20     /////
  ChordShape("7sus2",[0,2,7,10]),
  ChordShape("7sus4",[0,5,7,10]),
  ChordShape("min7",[0,3,7,10]),
  ChordShape("dim7",[0,3,6,8]),
  ChordShape("Maj9",[0,4,7,11,14]),

  ChordShape("Maj6/9",[0,4,7,9,14]),
  ChordShape("Maj#11",[0,4,7,11,14,18],2),
  ChordShape("9",[0,4,7,10,14]),
  ChordShape("7(b9)",[0,4,7,10,13]),
  ChordShape("7(b9,b13)",[0,4,7,10,13,20],2),
  #////////     30     /////
  ChordShape("Ionian",[0,2,4,5,7,9,11]),
  ChordShape("Dorian",[0,2,3,5,7,9,10]),
  ChordShape("Phrygian",[0,1,3,5,7,8,10]),
  ChordShape("Lydian",[0,2,4,6,7,9,11]),
  ChordShape("Mixolyd.",[0,2,4,5,7,9,10]),

  ChordShape("Aeolian",[0,2,3,5,7,8,10]),
  ChordShape("Locrian",[0,1,3,5,6,8,10]),
  ChordShape("Harm Min",[0,2,3,5,7,8,11]),
  ChordShape("Mel Min",[0,2,3,5,7,9,11]),
  ChordShape("Penta",[0,2,4,7,9]),
  #//////////    40 ////////
  ChordShape("min Penta",[0,3,5,7,10]),
  ChordShape("Maj Blues",[0,2,3,4,7,9]),
  ChordShape("min Blues",[0,3,5,6,7,10]),
  ChordShape("Bebop",[0,2,4,5,7,9,10,11]),
  ChordShape("WholeTone",[0,2,4,6,8,10]),

  ChordShape("Dim 1 1/2",[0,2,3,5,6,8,9,11]),
  ChordShape("Dim 1/2 1",[0,2,3,5,6,8,9,11]),
  ChordShape("Altered",[0,1,3,4,6,8,10]),
  ChordShape("Chromatic",[0,1,2,3,4,5,6,7,8,9,10,11]),
  ChordShape("All 4th",[0,5,10,15,20,26,31],3),
  #//////////    50 ////////
  ChordShape("All 5th",[0,7,14,21,28,35,41],4)
]
CHORD_MAP = {}

for ch in CHORD_SHAPES:
    CHORD_MAP[ch.chord_name] = ch
    CHORD_MAP[ch.chord_name.lower()] = ch
CHORD_MAP['maj'] = CHORD_MAP['Maj triad']
CHORD_MAP['min'] = CHORD_MAP['min triad']
CHORD_MAP['dim'] = CHORD_MAP['dim triad']
CHORD_MAP['aug'] = CHORD_MAP['aug triad']


def find_chord(chord_desc):
    chord = None
    if type(chord_desc) == str:
        chord = CHORD_MAP[chord_desc]
    else:
        chord = CHORD_SHAPES[chord_desc % len(CHORD_SHAPES)]
    if chord is None:
        raise("chord not found: " + chord_desc)
    return chord


MAJOR_KEY_CHORDS = [
    Chord(find_chord("Maj triad"),0),  #C   I
    Chord(find_chord("min triad"),2),  #D   ii
    Chord(find_chord("min triad"),4),  #E   iii
    Chord(find_chord("Maj triad"),5),  #F   IV
    Chord(find_chord("Maj triad"),7),  #G   V
    Chord(find_chord("min triad"),-3),  #A   vi
    Chord(find_chord("dim triad"),-1)  #B   viio Diminished triad
]
MINOR_KEY_CHORDS = [
    Chord(find_chord("min triad"),0),  #C   i
    Chord(find_chord("dim triad"),2),  #D   iio Diminished triad
    Chord(find_chord("aug triad"),4),  #E   III+ Augmented triad
    Chord(find_chord("min triad"),5),  #F   iv
    Chord(find_chord("Maj triad"),7),  #G   V
    Chord(find_chord("Maj triad"),-3),  #A   VI
    Chord(find_chord("dim triad"),-1)  #B   viio Diminished triad
]
