from midi.StrumPattern import StrumPattern
from midi.MidiServer import *
from midi.Rhythms import RhythmModule, MpcDrumKit, MpcPadsChromaticMidi0, Spark, VolcaBeats, MOTORIK3
from midi.Carpeggio import Carpeggio, CarpeggioRand, CarpeggioGenerative

app = MidiServer()
q = app.patchQueue


#
# CLOCK
#

app.useExternalClock('IAC Driver Bus 1_clock')
#app.useInternalClock(90)


#
# MODULES
#

StrumPattern(q, 'strumpattern')
DebugModule(q, 'debug')
m = RhythmModule(q, "rhythm", drumkit=MpcPadsChromaticMidi0(8), channel=CH10, ppq=PPQ)
m.instrument = [0,2,3,5]
CarpeggioGenerative(q, "carpeggio", channel=CH9, drone=CH8, ppq=PPQ, minor=False)

# 
# PATCH!
#

# sequencer needs clock, and supports control_change messages
app.patch('clock','rhythm_clock_in')
app.patch('knobs','rhythm_cc_in')
# send to MPC
app.patch('rhythm_out','instrument')
#app.patch('rhythm_out','debug')

# sequencer needs clock, and supports control_change messages
app.patch('clock','carpeggio_clock_in')
#app.patch('knobs','carpeggio_cc_in')
# send to MPC
app.patch('carpeggio_out','instrument')
#app.patch('carpeggio_out','debug')

# pass through keyboard to instrument for testing
#self.patch('keyboard','instrument')


import cProfile
cProfile.run('app.main()')
#app.main()