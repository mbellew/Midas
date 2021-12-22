import sys
from app.StrumPattern import StrumPattern
from app.Application import DebugModule, Application, PPQ
from app.Rhythms import RhythmModule


app = Application()
q = app.patchQueue

#
# MODULES
#

StrumPattern(q, 'strumpattern_in', 'strumpattern_out')
DebugModule(q, 'debug')
RhythmModule(q, "rhythm_clock_in", "rhythm_cc_in", "rhythm_beat_out", channel=9, ppq=PPQ)

# 
# PATCH!
#

# USE THIS IF THERE IS NO EXTERNAL MIDI CLOCK
#self.patch('internal_clock','timekeeper_in'
#self.patch('knobs','internal_clock_cc')

# get clock from MPC over IAC Bus
app.patch('IAC Driver Bus 1_clock','timekeeper_in')

# sequencer needs clock
app.patch('clock','rhythm_clock_in')

# CC control of rhythm  sequencer
app.patch('knobs','rhythm_cc_in')

# send to MPC
app.patch('rhythm_beat_out','instrument')

# debug output
#self.patch('rhythm_beat_out','debug')

# pass through keyboard to instrument for testing
#self.patch('keyboard','instrument')

app.main()