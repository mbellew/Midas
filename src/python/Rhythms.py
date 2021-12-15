from Event import * 
import mido
import random


Rhythm_array = []
 
class Rhythm:

    def __init__(self, count, str):
        global Rhythm_array
        self.count = count
        self.parts = []
        str = str.lower()
        arr = str.split("\n")
        for s in arr:
            s = s.strip().replace("_",".").replace(' ',".")[0:count]
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
        self.notes = [60,64,67,72]
        #self.notes = [1,2,3,4]
        self.offsets = [0,0,0,0]
        #self.offsets = [0,2,3,5]
        self.probability = [1,1,1,1]
        #self.probability = [1,0.9,0.90,0.70]
        self.time = 0

    def next(self):
        ret = [0, 0, 0, 0]
        for i in range(0,4):
            t = (self.time + self.offsets[i]) % self.rhythm.count
            ret[i] = 0 if self.rhythm.parts[i][t]=='.' else self.notes[i]
            if ret[i] and self.probability[i] < 1 and random.random() > self.probability[i]:
                ret[i] = 0
        self.time = (self.time + 1) % self.rhythm.count
        return ret


# Move to own .py
class MidiMap:
    def __init__(self):
        self.map = []

    def add(self, cc, lamb):
        while len(self.map) <= cc:
            self.map.append(None)
        self.map[cc] = lamb
    
    def dispatch(self,msg):
        if msg.control < len(self.map) and self.map[msg.control]:
             self.map[msg.control](msg)

class RhythmModule:
    def __init__(self, q, clock_sink, cc_sink, notes_out, Rhythm):
        q.createSink(clock_sink,self)
        q.createSink(cc_sink,self)
        self.notes_out = q.createSource(notes_out)
        self.player = Player(Rhythm)
        self.ccmap = MidiMap()
        self.ccmap.add( 0, lambda m : self.cc_rhythm(m))
        self.ccmap.add( 4, lambda m : self.cc_offset(m,1))
        self.ccmap.add( 9, lambda m : self.cc_offset(m,2))
        self.ccmap.add(12, lambda m : self.cc_offset(m,3))
        self.ccmap.add( 1, lambda m : self.cc_prob(m,0))
        self.ccmap.add( 5, lambda m : self.cc_prob(m,1))
        self.ccmap.add( 9, lambda m : self.cc_prob(m,2))
        self.ccmap.add(13, lambda m : self.cc_prob(m,3))

    def cc_rhythm(self, msg):
        r = int((msg.value/128.0) * Rhythm.count())
        self.player.rhythm = Rhythm.get(r)

    def cc_offset(self, msg, c):
        count = self.player.rhythm.count
        offset = int((msg.value/128.0) * count)
        self.player.offsets[c] = offset

    def cc_prob(self, msg, c):
        count = self.player.rhythm.count
        p = msg.value/127.0
        self.player.probability[c] = p

    def handle(self, event):
        if event.code == EVENT_CLOCK:
            if event.obj.pos != 0:
                return
            for i in range(0,4):
                self.notes_out.add(Event(EVENT_MIDI,'debug',mido.Message('note_off',note=self.player.notes[i])))
            notes = self.player.next()
            for note in notes:
                if note:
                    self.notes_out.add(Event(EVENT_MIDI,'debug',mido.Message('note_on',note=note)))
        if event.code == EVENT_MIDI:
            #control_change channel=0 control=0 value=107 time=0
            msg = event.obj
            if msg.type == 'control_change':
                self.ccmap.dispatch(msg)

                # if msg.control == 0:
                #     r = int((msg.value/128.0) * Rhythm.count())
                #     self.player.rhythm = Rhythm.get(r)
                # if msg.control == 4 or msg.control == 8 or msg.control == 12:
                #     i = int((msg.control-0)/4)
                #     count = self.player.rhythm.count
                #     offset = int((msg.value/128.0) * count)
                #     self.player.offsets[i] = offset
                # if msg.control == 1 or msg.control == 5 or msg.control == 9 or msg.control == 13:
                #     i = int((msg.control-1)/4)
                #     count = self.player.rhythm.count
                #     p = msg.value/127.0
                #     self.player.probability[i] = p