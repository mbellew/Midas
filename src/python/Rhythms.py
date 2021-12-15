from Event import * 
import mido
import random

class Rhythm:
    def __init__(self, count, str):
        self.count = count
        self.parts = []
        str = str.lower()
        arr = str.split("\n")
        for s in arr:
            s = s.lstrip().replace("_",".").replace(' ',".")[0:count]
            if len(s) == 0:
                continue
            if len(s) < count:
                s = s + "..................................................."[0:count-len(s)]
            if len(s) != count:
                raise Exception("BAD")
            self.parts.append(s)
        if len(self.parts) != 4:
            raise Exception("BAD")


    def print(self):
        for p in self.parts:
            print(p)
        return


RHUMBA = Rhythm(16, """
    x__x___x__x_x___
    x__x___x__x_x___
    x_xx_x_xx_x_xx_x
    __xx__xx__x___xx
""")
JHAPTAL1 = Rhythm(10, """
    _x__xxx__x
    _x__xxx__x
    x_xx___xx_
    x____x____
""")
JHAPTAL2 = Rhythm(10, """
    x_________
    x_xx___xx_
    x_xx___xx_
    x____x____
""")
CHACHAR = Rhythm(32,"""
    x_______________x_______________
    x_______x_x_____x_______x_x_____
    ____x_______x_______x_______x___
    ______________________________xx
""")
MATA = Rhythm(18,"""
    x_________________
    x___x_x_____x__x__
    x___x_x_____xx_x_x
    ________x_____x__x
""")
PASHTO = Rhythm(14, """
    x_____________
    ____xx______x_
    ____xx______x_
    x_____x___x___
""")
PRIME232 = Rhythm(12, """
    x___________
    x.....x.....
    x x x x x x.
    xxxxxxxxxxxx     
""")


class Player:
    def __init__(self,Rhythm):
        self.Rhythm = Rhythm
        self.offsets = [0,0,0,0]
        self.notes = [60,64,67,72]
        self.probability = [1,0.95,0.90,0.85]
        self.time = 0

    def next(self):
        ret = [0, 0, 0, 0]
        for i in range(0,4):
            t = (self.time + self.offsets[i]) % self.Rhythm.count
            ret[i] = 0 if self.Rhythm.parts[i][t]=='.' else self.notes[i]
            if ret[i] and self.probability[i] < 1 and random.random() > self.probability[i]:
                ret[i] = 0
        self.time = (self.time + 1) % self.Rhythm.count
        return ret


class RhythmModule:
    def __init__(self, q, clock_sink, notes_out, Rhythm):
        q.createSink(clock_sink,self)
        self.notes_out = q.createSource(notes_out)
        self.player = Player(Rhythm)

    def handle(self, event):
        if event.code != EVENT_CLOCK:
            return
        if event.obj.pos != 0:
            return
        for i in range(0,4):
            self.notes_out.add(Event(EVENT_MIDI,'debug',mido.Message('note_off',note=self.player.notes[i])))
        notes = self.player.next()
        for note in notes:
            if note:
                self.notes_out.add(Event(EVENT_MIDI,'debug',mido.Message('note_on',note=note)))
