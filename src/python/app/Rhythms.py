from app.Event import * 
import mido
import random
from app.MidiMap import MidiMap


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

class NotesDrumKit(DrumKit):
    def __init__(self, notes):
        instruments = []
        for i in range(0,len(notes)):
            inst = {'on':mido.Message('note_on',note=notes[i]), 'off':mido.Message('note_off',note=notes[i]) }
            instruments.append(inst)
        super().__init__(instruments)

class VolcaBeats(NotesDrumKit):
    def __init__(self):
        super().__init__([36, 38, 43, 50, 42, 46, 39, 75, 67, 49])

class MpcDrumTrack(NotesDrumKit):
    def __init__(self):
        # C2 Major
        super().__init__([36,38,40,41,43,45,47, 48,50,52,53,55,57,59])

class Spark(NotesDrumKit):
    def __init__(self):
        # C2 Chromatic
        super().__init__([60,61,62,63,64,65,66,67,68,69,70,71, 72,73,74,75])

class RhythmModule:
    def __init__(self, q, clock_sink, cc_sink, notes_out, rhythm=POP1, drumkit=None, channel=10, ppq=48):
        q.createSink(clock_sink,self)
        q.createSink(cc_sink,self)
        self.ppq = ppq
        self.notes_out = q.createSource(notes_out)

        self.channel = channel
        self.drumkit = drumkit if drumkit else Spark()
        self.instrument = [0,1,2,3]
        self.notes_currently_on = []

        self.player = Player(rhythm)
        self.ccmap = MidiMap()
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

    def handle(self, event):
        if event.code == EVENT_CLOCK:
            if event.obj.pulse != 0 and event.obj.pulse != self.ppq/2:
                return
            for off_msg in self.notes_currently_on:
                self.notes_out.add(Event(EVENT_MIDI,'debug',off_msg))
                self.notes_currently_on = []
            parts = self.player.next()
            for part in parts:
                if part is not None:
                    on_msg = self.drumkit.note_on(self.instrument[part])
                    on_msg.channel = self.channel
                    off_msg = self.drumkit.note_off(self.instrument[part])
                    off_msg.channel = self.channel
                    self.notes_currently_on.append(off_msg)
                    self.notes_out.add(Event(EVENT_MIDI,'rhythms',on_msg))
        if event.code == EVENT_MIDI:
            msg = event.obj
            if msg.type == 'control_change':
                self.ccmap.dispatch(msg)
