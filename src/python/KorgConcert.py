from app.StrumPattern import StrumPattern
from app.Application import *
from app.Rhythms import RhythmModule, MpcDrumKit, MpcPadsChromaticMidi0, Spark, VolcaBeats, MOTORIK3
from app.Carpeggio import Carpeggio, CarpeggioRand, CarpeggioGenerative

app = Application()
q = app.patchQueue

#
# MODULES
#

# TODO how to setup/register modules with UI?

StrumPattern(q, 'strumpattern_in', 'strumpattern_out')
DebugModule(q, 'debug')
rm = RhythmModule(q, "rhythm_clock_in", "rhythm_cc_in", "rhythm_out", drumkit=VolcaBeats(), channel=CH10, ppq=PPQ)
rm.display_area = app.display_area.subArea(5,5,10,app.display_area.width-20)
rm.update_display()
CarpeggioGenerative(q, "carpeggio_clock_in", "carpeggio_cc_in", "carpeggio_out", "carpeggio_drone", ppq=PPQ, root=48, minor=True)

# 
# Configure OUTPUT channels
#

droneOut = app.getOutputChannel(CH8)
droneOut.setup('mio_sink', name="DRONE")

arpOut = app.getOutputChannel(CH9)
arpOut.setup('mio_sink', name="ARP")

drumOut = app.getOutputChannel(CH10)
drumOut.setup('mio_sink', name="DRUMS")

# 
# PATCH!
#

# USE THIS IF THERE IS NO EXTERNAL MIDI CLOCK
#app.patch('internal_clock','timekeeper_in')
app.patch('knobs','internal_clock_cc')

# get clock from MPC over IAC Bus
#app.patch('IAC Driver Bus 1_clock','timekeeper_in')
app.patch('mio_clock','timekeeper_in')

# sequencer needs clock, and supports control_change messages
app.patch('clock','rhythm_clock_in')
app.patch('knobs','rhythm_cc_in')
# send to MPC
app.patch('rhythm_out','CH10')
app.patch('rhythm_out','debug')

# sequencer needs clock, and supports control_change messages
app.patch('clock','carpeggio_clock_in')
app.patch('knobs','carpeggio_cc_in')
# send to MPC
app.patch('carpeggio_out','CH9')   
app.patch('carpeggio_drone','CH8')   
app.patch('carpeggio_out','debug')

# pass through keyboard to instrument for testing
#app.patch('keyboard','mio_sink')

app.main()
