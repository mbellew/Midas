from app.StrumPattern import StrumPattern
from app.Application import *
from app.Rhythms import RhythmModule, MpcDrumKit, MpcPadsChromaticMidi0, Spark, VolcaBeats, MOTORIK3
from app.Carpeggio import Carpeggio, CarpeggioRand, CarpeggioGenerative

app = Application()
q = app.patchQueue


#
# CLOCK
#

app.useExternalClock('IAC Driver Bus 1_clock')
#app.useInternalClock(90)


#
# MODULES
#

StrumPattern(q, 'strumpattern_in', 'strumpattern_out')
DebugModule(q, 'debug')
m = RhythmModule(q, "rhythm_clock_in", "rhythm_cc_in", "rhythm_out", drumkit=MpcPadsChromaticMidi0(8), channel=CH10, ppq=PPQ)
m.instrument = [0,2,3,5]
CarpeggioGenerative(q, "carpeggio_clock_in", "carpeggio_cc_in", "carpeggio_out", channel=CH9, drone=CH8, ppq=PPQ, minor=False)

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