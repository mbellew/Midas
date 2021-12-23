from app.StrumPattern import StrumPattern
from app.Application import DebugModule, Application, PPQ
from app.Rhythms import RhythmModule, MpcDrumTrack, Spark, VolcaBeats
from app.Carpeggio import Carpeggio, CarpeggioRand, CarpeggioGenerative

app = Application()
q = app.patchQueue

#
# MODULES
#

StrumPattern(q, 'strumpattern_in', 'strumpattern_out')
DebugModule(q, 'debug')
#RhythmModule(q, "rhythm_clock_in", "rhythm_cc_in", "rhythm_out", drumkit=MpcDrumTrack(), channel=9, ppq=PPQ)
RhythmModule(q, "rhythm_clock_in", "rhythm_cc_in", "rhythm_out", drumkit=Spark(), channel=9, ppq=PPQ)
CarpeggioGenerative(q, "carpeggio_clock_in", "carpeggio_cc_in", "carpeggio_out", channel=8, drone=7, ppq=PPQ)

# 
# PATCH!
#

# USE THIS IF THERE IS NO EXTERNAL MIDI CLOCK
#self.patch('internal_clock','timekeeper_in'
#self.patch('knobs','internal_clock_cc')

# get clock from MPC over IAC Bus
app.patch('IAC Driver Bus 1_clock','timekeeper_in')

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

app.main()