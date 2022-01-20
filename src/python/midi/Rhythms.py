import random

import mido

from midi.Euclidian import densifier
from midi.Event import *
from midi.Module import ProgramModule

Rhythm_array = []
 
class Rhythm:

    def __init__(self):
        self.name = None
        self.count = 0
        self.parts = []


    def init(self, name, count, rhythm_str, parts=4):
        global Rhythm_array
        self.name = name
        self.count = count
        rhythm_str = rhythm_str.lower()
        arr = rhythm_str.split("\n")
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
        if len(self.parts) != parts:
            raise Exception("expected " + str(parts) + " parts, found " + str(len(self.parts)))
        Rhythm_array.append(self)


    @staticmethod
    def create(name, count, rhythm_str, parts=4):
        r = Rhythm()
        r.init(name,count,rhythm_str,parts)
        return r


    @staticmethod
    def copy(from_):
        ret = Rhythm()
        ret.name = from_.name
        ret.count = from_.count
        ret.parts = from_.parts.copy()
        return ret
        

    @staticmethod
    def count():
        return len(Rhythm_array)

    @staticmethod
    def get(i):
        return Rhythm_array[i]

    def print(self):
        for p in self.parts:
            print(p)
        return

MOTORIK1 = Rhythm.create("MOTORIK1",32,"""
    |X xx      xx    X xx      xx    |
    |x   x   x   x   x x x    x  x x |
    |    x xx    x xx    x xx    x xx|
    |x   x   x   x   x   x   x   x   |
""")
MOTORIK2 = Rhythm.create("MOTORIK2",32,"""
    |X x x x x x x x X x x x x x x x |
    |    x       x       x       x  x|
    |x x   x x x   x x x   x x x     |
    |x   x   x   x   x   x   x   x   |
""")
MOTORIK3 = Rhythm.create("MOTORIK3",32,"""
    |Xx      x x     Xx      x x     |
    |    x       x       x       x x |
    |x xxx  xx xxx  xx xxx  xx xxx  x|
    |x       x x   x x               |
""")
POP1 = Rhythm.create("POP1",32,"""
    |X   x   x   x   X   x   x   x x |
    |  x  x  x xx      x  x  x xx  x |
    |    x       x       x       x  x|
    |x x x x x x x x x x x x x x x xx| 
""")
POP2=Rhythm.create("POP2",32,"""
    |  x x xxx x   xxx x   xxx x   x |
    |  x x xxx x   xxx x   xxx x   x |
    |    x       x       x       x   |
    |    x       x       x       x   |
""")
POP3 = Rhythm.create("POP3",32,"""
    |X x xxxxx x   xxX x   xxx x x   |
    |x x xxxxx x   xxx x   xxx x x   |
    |        x x     x x     x x   x |
    |        x x     x x     x x   x |
""")
POP4 = Rhythm.create("POP4",32,"""
    |X xx xx     xxxxX xx xx     xxxx|
    |x xx xx     xxxxx xx xx     xxxx|
    |xxxxx x   x xxxxx x   xxx x xx  |
    |xxxxx x   x xxxxx x   xxx x xx  |
""")
FUNK1 = Rhythm.create("FUNK1",16,"""
    |X  x x  x  x x  |
    |  x   x   x   x |
    | x x x x x x x x|
    | x   x   x   xxx|
""")
FUNK2 = Rhythm.create("FUNK2",16,"""
    |..x...x...x...x.
    |x xx xxxx x  xxx
    | x x x x x x x x
    | x   x   x   xxx
""")
FUNK3 = Rhythm.create("FUNK3",16,"""
    |X xx xxxx x  xxx
    |x  xx  xx  xx x 
    | x x x x x x x x 
    | x   x   x   xxx
""")
FUNK4 = Rhythm.create("FUNK4",16,"""
    |X  xx  xX  xx x.| 
    |x  x x  x  x x..|
    | x x x x x x x x|
    | x   x   x   xxx|
""")
POST = Rhythm.create("POST",20,"""
    |x..x.x.xxx..x.x.x.x.|
    |x        x          |
    |   x        x x x x |
    |x   x   x   x   x   |
""")
SEQUENCE = Rhythm.create("SEQUENCE",4,"""
    |x   |
    | x  |
    |  x |
    |   x|
""")
KING1 = Rhythm.create("KING1",12,"""
    |x x xx x x x|
    |x x xx x x x|
    |x xx x  xx  |
    |x xx x  xx  |
""")
KING2 = Rhythm.create("KING2",12,"""
    |x xx x  xx  |
    |x xx x   x  |
    |x x xx x x x|
    |x x xx x x x|
""")
KROBOTO = Rhythm.create("KROBOTO",12,"""
    |  x xx  x xx|
    |  x xx  x xx|
    |x     x  x  |
    |x x xx x x x|  
""")
VODOU1 = Rhythm.create("VODOU1",12,"""
    |x x x xx x x|
    |x x x xx x x|
    |x     x  x  |
    |    xx    xx|
""")
VODOU2 = Rhythm.create("VODOU2",12, """
    | xx xx xx xx|
    | xx xx xx xx|
    |x x x xx x x|
    |    xx    xx|
""")
VODOU3 = Rhythm.create("VODOU3",12, """
    |x     x  x  |
    |x     x  x  |
    | xx xx xx xx|
    |    xx    xx|
""")
GAHU = Rhythm.create("GAHU",16, """
    |Xx x x x x x x  |
    |xx x x x x x x  |
    |x  . . . . . .  |
    |x  x   x   x x  |
""")
CLAVE = Rhythm.create("CLAVE",16, """
    |X  x  x   x x   |
    |x  x  x   x x   |
    |x xx x xx x xx x|
    |  xx  xx  x   xx|
""")
RHUMBA = Rhythm.create("RHUMBA",16, """
    |X__x___x__x_x___
    |x__x___x__x_x___
    |x_xx_x_xx_x_xx_x
    |__xx__xx__x___xx
""")
JHAPTAL1 = Rhythm.create("JHAPTAL1",10, """
    |_x__xxx__x
    |_x__xxx__x
    |x_xx___xx_
    |x____x____
""")
JHAPTAL2 = Rhythm.create("JHAPTAL2",10, """
    |x_________
    |x_xx___xx_
    |x_xx___xx_
    |x____x____
""")
CHACHAR = Rhythm.create("CHACHAR",32,"""
    |X_______________x_______________
    |x_______x_x_____x_______x_x_____
    |____x_______x_______x_______x___
    |______________________________xx
""")
MATA = Rhythm.create("MATA",18,"""
    |x_________________
    |x___x_x_____x__x__
    |x___x_x_____xx_x_x
    |________x_____x__x
""")
PASHTO = Rhythm.create("PASHTO",14, """
    |x_____________
    |____xx______x_
    |____xx______x_
    |x_____x___x___
""")
PRIME2 = Rhythm.create("PRIME2",8,"""
    |x
    |x   x
    |x x x x
    |xxxxxxxx
""")
PRIME322 = Rhythm.create("PRIME322",12,"""
    |x
    |x     x
    |x  x  x  x
    |xxxxxxxxxxxx
""")
PRIME232 = Rhythm.create("PRIME232",12, """
    |x
    |x     x
    |x x x x x x
    |xxxxxxxxxxxx     
""")

BOOTSNCATS = Rhythm.create("BOOTSNCATS",8, 
    "|x       |\n" +  # KICK 1
    "|    x   |\n" +  # KICK 2 (can be same as KICK1)
    "|    x   |\n" +  # SNARE
    "|    x   |\n" +  # REINFORCEMENT
    "|  xx  x |\n" +  # HAT
    "|x x x x |",      # TICKTICKTICK
    parts=6
)
# TODO for end of bar/section
BOOTSNCATS_ACCENT = Rhythm.create("BOOTSNCATS",8, 
    "|x       |\n" +  # KICK 1
    "|    x   |\n" +  # KICK 2 (can be same as KICK1)
    "|    x   |\n" +  # SNARE
    "|    x   |\n" +  # REINFORCEMENT
    "|  xx  x |\n" +  # HAT
    "|x x x x |",      # TICKTICKTICK
    parts=6
)


class Player:
    def __init__(self,rhythm):
        self.rhythm = rhythm
        self.offsets = [0] * len(rhythm.parts)
        self.probability = [1]  * len(rhythm.parts)
        self.time = 0

    # returns a 4 element array with velocities
    def next(self):
        count = len(self.rhythm.parts)
        ret = [0] * count
        for i in range(0,count):
            t = (self.time + self.offsets[i]) % self.rhythm.count
            ch = self.rhythm.parts[i][t]
            if ch == '.' or ch ==' ':
                continue
            if self.probability[i] < 1 and random.random() > self.probability[i]:
                continue
            ret[i] = 127 if ch == 'X' else 64
        self.time = (self.time + 1) % self.rhythm.count
        return ret

    def update_display(self, area):
        for i in range(0,len(self.rhythm.parts)):
            off = self.offsets[i] % self.rhythm.count
            pattern = self.rhythm.parts[i]
            area.write(i,0,pattern[off:] + pattern[0:off])
            area.right(i,len(pattern)+1,str(int(self.probability[i]*100))+'%',pad=4)


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


class CircuitTrackDrumKit(NotesDrumKit):
    def __init__(self):
        #super().__init__([36, 38, 40, 41])
        #super().__init__([48, 50, 52, 53])
        #super().__init__([24, 26, 28, 29])
        super().__init__([60, 62, 64, 65])


# Key mapping seems to vary by drum kit!, but often follows GeneralMidiDrum numbering
# recommend using "Edit/Program/Note Mapping..." to pick a predefined key mapping OR match Spark() pattern C6 semi-tones
class MpcDrumKit(NotesDrumKit):
    def __init__(self):
        # C2 Major
        super().__init__([36,38,40,41,43,45,47, 48,50,52,53,55,57,59])

# This is built-in MPC mapping "Chromatic C1"
class MpcPadsChromaticC1(NotesDrumKit):
    def __init__(self, count=8):
        super().__init__(range(36,36+count))

# This is built-in MPC mapping "Chromatic C-2"
class MpcPadsChromaticMidi0(NotesDrumKit):
    def __init__(self, count=8):
        super().__init__(range(0,count))

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


class RhythmModule(ProgramModule):
    def __init__(self, q, name, rhythm=POP1, drumkit=MpcPadsChromaticC1(), channel=9, ppq=24):
        super().__init__("Rhythms")
        self.current_rhythm = rhythm
        self.density_patterns = [None, None, None, None]
        self.double_time = False
        q.createSink(name + "_in", self)
        q.createSink(name + "_clock_in", self)
        self.cc_sink = q.createSink(name + "_cc_in", self)
        self.ppq = ppq
        self.notes_out = q.createSource(name + "_out")
        # OUTPUT note_on events to act as gate, DOES NOT SEND note_off
        self.trigger_out = [
            q.createSource(name + "_trigger1"),
            q.createSource(name + "_trigger2"),
            q.createSource(name + "_trigger3"),
            q.createSource(name + "_trigger4")
        ]

        self.channel = channel
        self.drumkit = drumkit if drumkit else Spark()
        self.instrument = [0,1,2,3]
        self.notes_currently_on = []

        self.player = Player(Rhythm.copy(rhythm))
        print(self.player.rhythm.name)
        self.ccmap.add( 0, lambda m : self.cc_rhythm(m))
        self.ccmap.add( 4, lambda m : self.cc_offset(m,1))
        self.ccmap.add( 8, lambda m : self.cc_offset(m,2))
        self.ccmap.add(12, lambda m : self.cc_offset(m,3))

        self.ccmap.add( 1, lambda m : self.cc_prob(m,0))
        self.ccmap.add( 5, lambda m : self.cc_prob(m,1))
        self.ccmap.add( 9, lambda m : self.cc_prob(m,2))
        self.ccmap.add(13, lambda m : self.cc_prob(m,3))

        self.ccmap.add( 2, lambda m : self.cc_instrument(m,0))
        self.ccmap.add( 6, lambda m : self.cc_instrument(m,1))
        self.ccmap.add(10, lambda m : self.cc_instrument(m,2))
        self.ccmap.add(14, lambda m : self.cc_instrument(m,3))

        self.ccmap.add( 3, lambda m : self.cc_density(m, 0))
        self.ccmap.add( 7, lambda m : self.cc_density(m, 1))
        self.ccmap.add(11, lambda m : self.cc_density(m, 2))
        self.ccmap.add(15, lambda m : self.cc_density(m, 3))

    def get_control_sink(self):
        return self.cc_sink

    def get_display_name(self):
        return self.name + " " + self.player.rhythm.name

    def update_display(self):
        for i in range(0,4):
            self.display_area.right(i,0,str(self.instrument[i]),pad=2)
        self.player.update_display(self.display_area.subArea(0,3,4,40))

    def cc_rhythm(self, msg):
        r = int((msg.value/128.0) * Rhythm.count())
        rhythm = Rhythm.get(r)
        if  self.current_rhythm != rhythm:
            self.density_patterns = [None, None, None, None]
            self.current_rhythm = rhythm
            self.player.rhythm = Rhythm.copy(rhythm)
            self.update_display()

    def cc_offset(self, msg, ch):
        rhythm_length = self.player.rhythm.count
        offset = int((1.0-msg.value/128.0) * rhythm_length)
        if self.player.offsets[ch] != offset:
            self.player.offsets[ch] = offset
            self.update_display()

    def cc_prob(self, msg, ch):
        p = msg.value/127.0
        self.player.probability[ch] = p
        self.update_display()

    def cc_instrument(self, msg, ch):
        count = self.drumkit.count()
        i = int((msg.value/128.0) * count)
        if self.instrument[ch] != i:
            self.instrument[ch] = i
            self.update_display()
            #print(self.instrument)

    def cc_density(self, msg, ch):
        if ch >= len(self.current_rhythm.parts):
            return
        rhythm_length = self.player.rhythm.count
        density = round((msg.value/127.0) * rhythm_length)
        # this is why we copy the rhythm, we hack it up here
        if not self.density_patterns[ch]:
            self.density_patterns[ch] = densifier(self.current_rhythm.parts[ch])
            print(self.current_rhythm.parts[ch].upper())
            print('\n'.join(self.density_patterns[ch]))
        arr = self.density_patterns[ch]
        new_str = arr[density]
        self.player.rhythm.parts[ch] = new_str
        self.update_display()


    def handle_clock(self, pulse):
        trigger = self.double_time and pulse.sixteenth or pulse.eighth
        if not trigger:
            return
        for off_msg in self.notes_currently_on:
            off_msg.time = self.time
            self.notes_out.add(Event(EVENT_MIDI,'rhythms',off_msg))
            self.notes_currently_on = []
        parts = self.player.next()
        for part in range(0,len(parts)):
            velocity = parts[part]
            instrument = self.instrument[part % len(self.instrument)]
            if velocity > 0 and instrument >= 0:
                on_msg = self.drumkit.note_on(self.instrument[part % len(self.instrument)])
                on_msg.velocity = velocity
                if self.channel is not None:
                    on_msg.channel = self.channel
                off_msg = self.drumkit.note_off(self.instrument[part])
                if self.channel is not None:
                    off_msg.channel = self.channel
                self.notes_currently_on.append(off_msg)
                on_msg.time = self.time
                evt = Event(EVENT_MIDI,'rhythms',on_msg)
                self.notes_out.add(evt)
                if part < 4:
                    self.trigger_out[part].add(evt)
 
    def handle_stop(self):
        for off_msg in self.notes_currently_on:
            off_msg.time = self.time
            self.notes_out.add(Event(EVENT_MIDI,'rhythms',off_msg))
        self.notes_currently_on = []

        for i in range(0,self.drumkit.count()):
            off_msg = self.drumkit.note_off(i)
            off_msg.time = self.time
            self.notes_out.add(Event(EVENT_MIDI,'rhythms',off_msg))
 


class BootsNCats(RhythmModule):
     def __init__(self, q, name, rhythm=BOOTSNCATS, instruments=None, drumkit=MpcPadsChromaticC1(), ppq=24):
         super().__init__(q, name, rhythm, drumkit, ppq=ppq)
         self.double_time = True
         if instruments is None:
            if isinstance(drumkit,VolcaBeats):
                instruments = [0, 0, 1, 6, 4, 7]  # KICK, KICK, SNARE, CLAP, CL HAT, CLAVE
            else:
                instruments = [1, 2, 3, 4, 5, 6]
         self.instrument = instruments


# BOOTSNCATS = Rhythm.create("BOOTSNCATS",8, 
#     "|x       |\n" +  # KICK 1
#     "|    x   |\n" +  # KICK 2 (can be same as KICK1)
#     "|    x   |\n" +  # SNARE
#     "|    x   |\n" +  # REINFORCEMENT
#     "|  xx  x |\n" +  # HAT
#     "|x x x x |"      # TICKTICKTICK
#     )