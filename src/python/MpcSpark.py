from midi.StrumPattern import StrumPattern
from midi.MidiServer import *
from midi.Rhythms import RhythmModule, MpcDrumKit, Spark, VolcaBeats, MOTORIK3
from midi.Carpeggio import Carpeggio, CarpeggioRand, CarpeggioGenerative

app = MidiServer()
q = app.patchQueue

#
# MODULES
#

StrumPattern(q, 'strumpattern')
DebugModule(q, 'debug')
RhythmModule(q, "rhythm", drumkit=Spark(60), channel=CH10, ppq=PPQ)
CarpeggioGenerative(q, "carpeggio", ppq=PPQ, minor=False)

# 
# PATCH!
#

# USE THIS IF THERE IS NO EXTERNAL MIDI CLOCK
# app.patch('internal_clock','timekeeper_in')
app.patch('knobs','internal_clock_cc')

# get clock from MPC over IAC Bus
app.patch('IAC Driver Bus 1_clock', 'timekeeper_in')

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