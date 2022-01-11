#!/usr/bin/python3
from midi.MidiServer import *
from midi.MidiServer import *
from midi.Carpeggio import CarpeggioGenerative
from midi.Rhythms import RhythmModule, CircuitTrackDrumKit

app = MidiServer()
q = app.patchQueue

#
# CLOCK
#

#app.useExternalClock('USB MIDI Interface_clock')
app.useInternalClock(90)

#
# MODULES
#

# Create the modules we want to use
# "Programs" are modules that have CC control and/or show up in the 'UI'
# TODO have addProgram() wire up clock_in and ppq

app.addProgramController('Arturia BeatStep_in', BEATSTEP_CONTROLLER)
app.addProgramController('Midi Fighter Twister_in', TWISTER_CONTROLLER)

DebugModule(q, 'debug')
app.addProgram(RhythmModule(q, "rhythm_clock_in", "rhythm_cc_in", "rhythm_out", drumkit=CircuitTrackDrumKit(), ppq=PPQ))
app.addProgram(CarpeggioGenerative(q, "carpeggio_clock_in", "carpeggio_cc_in", "carpeggio_out", "carpeggio_drone", ppq=PPQ, root=48, minor=True))


# 
# Configure OUTPUT channels
#

droneOut = app.setupOutputChannel(CH2, 'USB MIDI Interface_sink', name="DRONE")
arpOut = app.setupOutputChannel(CH1, 'USB MIDI Interface_sink', name="ARP")
drumOut = app.setupOutputChannel(CH10, 'USB MIDI Interface_sink', name="DRUMS")

# 
# PATCH!
#

# sequencer needs clock, and supports control_change messages
app.patch('clock', 'rhythm_clock_in')
app.patch('rhythm_out', drumOut)

# sequencer needs clock, and supports control_change messages
app.patch('clock', 'carpeggio_clock_in')
app.patch('carpeggio_out', arpOut)
app.patch('carpeggio_drone', droneOut)   

# app.patch('Arturia BeatStep_in','debug')
app.patch('Arturia KeyStep 37_in', 'CH10')
app.patch('Arturia KeyStep 37_in', 'debug')

app.main()
