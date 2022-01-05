from app.StrumPattern import StrumPattern
from app.Application import *
from app.Rhythms import RhythmModule, MpcDrumKit, MpcPadsChromaticMidi0, Spark, VolcaBeats, MOTORIK3
from app.Carpeggio import CarpeggioGenerative

app = Application()
q = app.patchQueue

#
# MODULES
#

# Create the modules we want to use
# "Programs" are modules that have CC control and/or show up in the 'UI'
# TODO have addProgram() wire up clock_in

app.addProgramController('Arturia BeatStep_in', BEATSTEP_CONTROLLER)
app.addProgramController('Midi Fighter Twister_in', TWISTER_CONTROLLER)

DebugModule(q, 'debug')
app.addProgram(RhythmModule(q, "rhythm_clock_in", "rhythm_cc_in", "rhythm_out", drumkit=VolcaBeats(), ppq=PPQ))
app.addProgram(CarpeggioGenerative(q, "carpeggio_clock_in", "carpeggio_cc_in", "carpeggio_out", "carpeggio_drone", ppq=PPQ, root=48, minor=True))


# 
# Configure OUTPUT channels
#

droneOut = app.setupOutputChannel(CH8, 'mio_sink', name="DRONE")
arpOut = app.setupOutputChannel(CH9, 'mio_sink', name="ARP")
drumOut = app.setupOutputChannel(CH10, 'mio_sink', name="DRUMS")

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
app.patch('rhythm_out', drumOut)

# sequencer needs clock, and supports control_change messages
app.patch('clock','carpeggio_clock_in')
app.patch('carpeggio_out', arpOut)
app.patch('carpeggio_drone', droneOut)   

# pass through keyboard to instrument for testing
#app.patch('keyboard','mio_sink')
#app.patch('Arturia BeatStep_in','debug')
#app.patch('knobs','debug')

app.main()
