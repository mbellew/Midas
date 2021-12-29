from app.Event import * 
from app.Module import AbstractModule
import mido
import random
from app.MidiMap import MidiMap
from app.Module import AbstractModule


Rhythm_array = []
 
class Rhythm:

    def __init__(self, count, str):
        global Rhythm_array
        self.count = count
        self.parts = []
        str = str.lower()
        arr = str.split("\n")
        for s in arr:
            s = s.strip().replace("_",".").replace(' ',".")
            if len(s) == 0:
                continue
            if s.startswith('|'):
                s = s[1:]
            if s.endswith('|'):
                s = s[0:len(s)-1]
            elif len(s) < count:
                s = s + "..................................................."[0:count-len(s)]
            if len(s) != count:
                raise Exception("BAD")
            self.parts.append(s)
        if len(self.parts) != 4:
            raise Exception("BAD")
        Rhythm_array.append(self)

    def count():
        return len(Rhythm_array)

    def get(i):
        return Rhythm_array[i]

    def print(self):
        for p in self.parts:
            print(p)
        return

MOTORIK1 = Rhythm(32,"""
    |x xx      xx    x xx      xx    |
    |x   x   x   x   x x x    x  x x |
    |    x xx    x xx    x xx    x xx|
    |x   x   x   x   x   x   x   x   |
""")
MOTORIK2 = Rhythm(32,"""
    |x x x x x x x x x x x x x x x x |
    |    x       x       x       x  x|
    |x x   x x x   x x x   x x x     |
    |x   x   x   x   x   x   x   x   |
""")
MOTORIK3 = Rhythm(32,"""
    |xx      x x     xx      x x     |
    |    x       x       x       x x |
    |x xxx  xx xxx  xx xxx  xx xxx  x|
    |x       x x   x x               |
""")
POP1 = Rhythm(32,"""
    |x   x   x   x   x   x   x   x x |
    |  x  x  x xx      x  x  x xx  x |
    |    x       x       x       x  x|
    |x x x x x x x x x x x x x x x xx| 
""")
POP2=Rhythm(32,"""
    |  x x xxx x   xxx x   xxx x   x |
    |  x x xxx x   xxx x   xxx x   x |
    |    x       x       x       x   |
    |    x       x       x       x   |
""")
POP3 = Rhythm(32,"""
    |x x xxxxx x   xxx x   xxx x x   |
    |x x xxxxx x   xxx x   xxx x x   |
    |        x x     x x     x x   x |
    |        x x     x x     x x   x |
""")
POP4 = Rhythm(32,"""
    |x xx xx     xxxxx xx xx     xxxx|
    |x xx xx     xxxxx xx xx     xxxx|
    |xxxxx x   x xxxxx x   xxx x xx  |
    |xxxxx x   x xxxxx x   xxx x xx  |
""")
FUNK1 = Rhythm(16,"""
    |x  x x  x  x x  |
    |  x   x   x   x |
    | x x x x x x x x|
    | x   x   x   xxx|
""")
FUNK2 = Rhythm(16,"""
    |..x...x...x...x.
    |x xx xxxx x  xxx
    | x x x x x x x x
    | x   x   x   xxx
""")
FUNK3 = Rhythm(16,"""
    |x xx xxxx x  xxx
    |x  xx  xx  xx x 
    | x x x x x x x x 
    | x   x   x   xxx
""")
FUNK4 = Rhythm(16,"""
    |x  xx  xx  xx x. 
    |x  x x  x  x x..
    | x x x x x x x x
    | x   x   x   xxx
""")
POST = Rhythm(20,"""
    |x..x.x.xxx..x.x.x.x.|
    |x        x          |
    |   x        x x x x |
    |x   x   x   x   x   |
""")
SEQUENCE = Rhythm(4,"""
    |x   |
    | x  |
    |  x |
    |   x|
""")
KING1 = Rhythm(12,"""
    |x x xx x x x|
    |x x xx x x x|
    |x xx x  xx  |
    |x xx x  xx  |
""")
KING2 = Rhythm(12,"""
    |x xx x  xx  |
    |x xx x   x  |
    |x x xx x x x|
    |x x xx x x x|
""")
KROBOTO = Rhythm(12,"""
    |  x xx  x xx|
    |  x xx  x xx|
    |x     x  x  |
    |x x xx x x x|  
""")
VODOU1 = Rhythm(12,"""
    |x x x xx x x|
    |x x x xx x x|
    |x     x  x  |
    |    xx    xx|
""")
VODOU2 = Rhythm(12, """
    | xx xx xx xx|
    | xx xx xx xx|
    |x x x xx x x|
    |    xx    xx|
""")
VODOU3 = Rhythm(12, """
    |x     x  x  |
    |x     x  x  |
    | xx xx xx xx|
    |    xx    xx|
""")
GAHU = Rhythm(16, """
    |xx x x x x x x  |
    |xx x x x x x x  |
    |x  . . . . . .  |
    |x  x   x   x x  |
""")
CLAVE = Rhythm(16, """
    |x  x  x   x x   |
    |x  x  x   x x   |
    |x xx x xx x xx x|
    |  xx  xx  x   xx|
""")
RHUMBA = Rhythm(16, """
    |x__x___x__x_x___
    |x__x___x__x_x___
    |x_xx_x_xx_x_xx_x
    |__xx__xx__x___xx
""")
JHAPTAL1 = Rhythm(10, """
    |_x__xxx__x
    |_x__xxx__x
    |x_xx___xx_
    |x____x____
""")
JHAPTAL2 = Rhythm(10, """
    |x_________
    |x_xx___xx_
    |x_xx___xx_
    |x____x____
""")
CHACHAR = Rhythm(32,"""
    |x_______________x_______________
    |x_______x_x_____x_______x_x_____
    |____x_______x_______x_______x___
    |______________________________xx
""")
MATA = Rhythm(18,"""
    |x_________________
    |x___x_x_____x__x__
    |x___x_x_____xx_x_x
    |________x_____x__x
""")
PASHTO = Rhythm(14, """
    |x_____________
    |____xx______x_
    |____xx______x_
    |x_____x___x___
""")
PRIME2 = Rhythm(8,"""
    |x
    |x   x
    |x x x x
    |xxxxxxxx
""")
PRIME322 = Rhythm(12,"""
    |x
    |x     x
    |x  x  x  x
    |xxxxxxxxxxxx
""")
PRIME232 = Rhythm(12, """
    |x
    |x     x
    |x x x x x x
    |xxxxxxxxxxxx     
""")


class Player:
    def __init__(self,rhythm):
        self.rhythm = rhythm
        self.offsets = [0,0,0,0]
        self.probability = [1,1,1,1]
        self.time = 0

    def next(self):
        ret = []
        for i in range(0,4):
            t = (self.time + self.offsets[i]) % self.rhythm.count
            if self.rhythm.parts[i][t] == '.':
                continue
            if self.probability[i] < 1 and random.random() > self.probability[i]:
                continue
            ret.append(i)
        self.time = (self.time + 1) % self.rhythm.count
        return ret



# This is really just a note remapping helper that deals with Drum kits, since they all have different mappings
# onto notes (or sometimes CC)
class DrumKit:
    def __init__(self, instruments):
        self.instruments = instruments

    # return a midi message
    def note_on(self, i):
        inst = self.instruments[i % len(self.instruments)]
        return inst['on']

    # return a midi message
    def note_off(self, i):
        inst = self.instruments[i % len(self.instruments)]
        return inst['off']

    def count(self) -> int:
        return len(self.instruments)

# https://soundprogramming.net/file-formats/general-midi-drum-note-numbers/
GeneralMidiDrumMap = {
    "High Q":27,
    "Slap":28,
    "Scratch Push":29,
    "Scratch Pull":30,
    "Sticks":31,
    "Square Click":32,
    "Metronome Click":33,
    "Metronome Bell":34,
    "Bass Drum 2":35,
    "Bass Drum 1":36,
    "Side Stick":37,
    "Snare Drum 1":38,
    "Hand Clap":39,
    "Snare Drum 2":40,
    "Low Tom 2":41,
    "Closed Hi-hat":42,
    "Low Tom 1":43,
    "Pedal Hi-hat":44,
    "Mid Tom 2":45,
    "Open Hi-hat":46,
    "Mid Tom 1":47,
    "High Tom 2":48,
    "Crash Cymbal 1":49,
    "High Tom 1":50,
    "Ride Cymbal 1":51,
    "Chinese Cymbal":52,
    "Ride Bell":53,
    "Tambourine":54,
    "Splash Cymbal":55,
    "Cowbell":56,
    "Crash Cymbal 2":57,
    "Vibra Slap":58,
    "Ride Cymbal 2":59,
    "High Bongo":60,
    "Low Bongo":61,
    "Mute High Conga":62,
    "Open High Conga":63,
    "Low Conga":64,
    "High Timbale":65,
    "Low Timbale":66,
    "High Agogo":67,
    "Low Agogo":68,
    "Cabasa":69,
    "Maracas":70,
    "Short Whistle":71,
    "Long Whistle":72,
    "Short Guiro":73,
    "Long Guiro":74,
    "Claves":75,
    "High Wood Block":76,
    "Low Wood Block":77,
    "Mute Cuica":78,
    "Open Cuica":79,
    "Mute Triangle":80,
    "Open Triangle":81,
    "Shaker":82,
    "Jingle Bell":83,
    "Belltree":84,
    "Castanets":85,
    "Mute Surdo":86,
    "Open Surdo":87
}
            

class NotesDrumKit(DrumKit):
    def __init__(self, notes):
        instruments = []
        for i in range(0,len(notes)):
            inst = {'on':mido.Message('note_on',note=notes[i]), 'off':mido.Message('note_off',note=notes[i]) }
            instruments.append(inst)
        super().__init__(instruments)   


class GeneralMidiDrumKit(NotesDrumKit):
    def __init__(self,names):
        global GeneralMidiDrumMap
        notes = []
        for name in names:
            if not name in GeneralMidiDrumMap:
                raise Exception("Drum not found: " + name)
            notes.append(GeneralMidiDrumMap[name])
            super().__init__(notes)


class VolcaBeats(GeneralMidiDrumKit):
    def __init__(self):
        #super().__init__([36, 38, 43, 50, 42, 46, 39, 75, 67, 49])
        super().__init__(["Bass Drum 1","Snare Drum 1","Low Tom 1","High Tom 1","Closed Hi-hat","Open Hi-hat",
            "Hand Clap","Claves","High Agogo","Crash Cymbal 1"])


# Key mapping seems to vary by drum kit!, but often follows GeneralMidiDrum numbering
# recommend using "Edit/Program/Note Mapping..." to pick a predefined key mapping OR match Spark() pattern C6 semi-tones
class MpcDrumKit(NotesDrumKit):
    def __init__(self):
        # C2 Major
        super().__init__([36,38,40,41,43,45,47, 48,50,52,53,55,57,59])

# This is built-in MPC mapping "Chromatic C1"
class MpcPadsChromaticC1(NotesDrumKit):
    def __init__(self):
        super().__init(range(36,36+16))

# This is built-in MPC mapping "Chromatic C-2"
class MpcPadsChromaticMidi0(NotesDrumKit):
    def __init__(self):
        super().__init__(range(0,16))

# This is built-in MPC mapping "Classic MPC"
class MpcPadsClassic(NotesDrumKit):
    def __init__(self):
        super().__init([37,36,42,82,40,38,46,44,48,47,45,43,49,55,51,53])


# Multiple track with a DrumSynth
#class MpcDrumTracks(DrumKit):
#    def __init__(self):
#        instruments = []
#        for channel in range(0,4):
#            on_msg  = mido.Message('note_on',channel=channel,note=48)
#            off_msg = mido.Message('note_off',channel=channel,note=48)
#            inst = {'on':on_msg, 'off':off_msg}
#            instruments.append(inst)
#        super().__init__(instruments)


# 16 sequential semi-tones starting at 60
class Spark(NotesDrumKit):
    def __init__(self, root=60):
        super().__init__(range(root,root+16))


class RhythmModule(AbstractModule):
    def __init__(self, q, clock_sink, cc_sink, notes_out, rhythm=POP1, drumkit=None, channel=9, ppq=48):
        super().__init__()
        q.createSink(clock_sink,self)
        q.createSink(cc_sink,self)
        self.ppq = ppq
        self.notes_out = q.createSource(notes_out)

        self.channel = channel
        self.drumkit = drumkit if drumkit else Spark()
        self.instrument = [0,1,2,3]
        self.notes_currently_on = []

        self.player = Player(rhythm)
        self.ccmap.add( 0, lambda m : self.cc_rhythm(m))
        self.ccmap.add( 4, lambda m : self.cc_offset(m,1))
        self.ccmap.add( 9, lambda m : self.cc_offset(m,2))
        self.ccmap.add(12, lambda m : self.cc_offset(m,3))
        self.ccmap.add( 1, lambda m : self.cc_prob(m,0))
        self.ccmap.add( 5, lambda m : self.cc_prob(m,1))
        self.ccmap.add( 9, lambda m : self.cc_prob(m,2))
        self.ccmap.add(13, lambda m : self.cc_prob(m,3))
        self.ccmap.add( 2, lambda m : self.cc_instrument(m,0))
        self.ccmap.add( 6, lambda m : self.cc_instrument(m,1))
        self.ccmap.add(10, lambda m : self.cc_instrument(m,2))
        self.ccmap.add(14, lambda m : self.cc_instrument(m,3))

    def cc_rhythm(self, msg):
        r = int((msg.value/128.0) * Rhythm.count())
        self.player.rhythm = Rhythm.get(r)

    def cc_offset(self, msg, ch):
        count = self.player.rhythm.count
        offset = int((msg.value/128.0) * count)
        self.player.offsets[ch] = offset

    def cc_prob(self, msg, ch):
        p = msg.value/127.0
        self.player.probability[ch] = p

    def cc_instrument(self, msg, ch):
        count = self.drumkit.count()
        i = int((msg.value/128.0) * count)
        self.instrument[ch] = i

    def handle_clock(self, pulse):
        if not pulse.eighth:
            return
        for off_msg in self.notes_currently_on:
            off_msg.time = self.time
            self.notes_out.add(Event(EVENT_MIDI,'rhythms',off_msg))
            self.notes_currently_on = []
        parts = self.player.next()
        for part in parts:
            if part is not None:
                on_msg = self.drumkit.note_on(self.instrument[part])
                if self.channel is not None:
                    on_msg.channel = self.channel
                off_msg = self.drumkit.note_off(self.instrument[part])
                if self.channel is not None:
                    off_msg.channel = self.channel
                self.notes_currently_on.append(off_msg)
                on_msg.time = self.time
                self.notes_out.add(Event(EVENT_MIDI,'rhythms',on_msg))
 
    def handle_stop(self):
        for off_msg in self.notes_currently_on:
            off_msg.time = self.time
            self.notes_out.add(Event(EVENT_MIDI,'rhythms',off_msg))
        self.notes_currently_on = []

        for i in range(0,self.drumkit.count()):
            off_msg = self.drumkit.note_off(i)
            off_msg.time = self.time
            self.notes_out.add(Event(EVENT_MIDI,'rhythms',off_msg))
 
