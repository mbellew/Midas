from midi.MidiServer import *
from midi.MidiServer import *
from midi.Carpeggio import CarpeggioGenerative
from midi.Rhythms import RhythmModule, VolcaBeats

app = MidiServer()
q = app.patchQueue

#
# CLOCK
#

app.useExternalClock('mio_clock')
#app.useInternalClock(90)


#
# MODULES
#

# Create the modules we want to use
# "Programs" are modules that have CC control and/or show up in the 'UI'
# TODO have addProgram() wire up clock_in

app.addProgramController('Arturia BeatStep_in', BEATSTEP_CONTROLLER)
app.addProgramController('Midi Fighter Twister_in', TWISTER_CONTROLLER)

DebugModule(q, 'debug')
# app.addProgram(RhythmModule(q, "rhythm", drumkit=VolcaBeats(), ppq=PPQ))
# app.addProgram(CarpeggioGenerative(q, "carpeggio_clock_in", "carpeggio_cc_in", "carpeggio_out", "carpeggio_drone", ppq=PPQ, root=48, minor=True))
#
#
# #
# # Configure OUTPUT channels
# #
#
# droneOut = app.setupOutputChannel(CH8, 'mio_sink', name="DRONE")
# arpOut = app.setupOutputChannel(CH9, 'mio_sink', name="ARP")
# drumOut = app.setupOutputChannel(CH10, 'mio_sink', name="DRUMS")
#
# #
# # PATCH!
# #
#
# # sequencer needs clock, and supports control_change messages
# app.patch('clock', 'rhythm_clock_in')
# app.patch('rhythm_out', drumOut)
#
# # sequencer needs clock, and supports control_change messages
# app.patch('clock', 'carpeggio_clock_in')
# app.patch('carpeggio_out', arpOut)
# app.patch('carpeggio_drone', droneOut)

# app.patch('keyboard','mio_sink')
#app.patch('Arturia BeatStep_in','debug')
app.patch('MIDI Mix_in','debug')

app.main()
