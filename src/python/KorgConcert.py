from Application import Application
from midi.MidiServer import *
from midi.Carpeggio import CarpeggioGenerative
from midi.Rhythms import RhythmModule, VolcaBeats

app = Application.create()
q = app.patchQueue

#
# CLOCK
#

# app.useExternalClock('mio_clock')
app.useInternalClock(90)


#
# MODULES
#

# Create the modules we want to use
# "Programs" are modules that have CC control and/or show up in the 'UI'
# TODO have addProgram() wire up clock_in and ppq

app.addProgramController('Arturia BeatStep_in', BEATSTEP_CONTROLLER)
app.addProgramController('Midi Fighter Twister_in', TWISTER_CONTROLLER)
app.addProgramController('MIDI Mix_in', AKAIMIDIMIX_CONTROLLER)

DebugModule(q, 'debug')
app.addProgram(RhythmModule(q, "rhythm_clock_in", "rhythm_cc_in", "rhythm_out", drumkit=VolcaBeats(), ppq=PPQ))
app.addProgram(CarpeggioGenerative(q, "carpeggio_clock_in", "carpeggio_cc_in", "carpeggio_out", "carpeggio_drone", ppq=PPQ, root=48, minor=True))


# 
# Configure OUTPUT channels
#

# TODO app.hasDevice('name')
output_device = 'Scarlett 4i4 USB_sink' if True else 'mio_sink'
droneOut = app.setupOutputChannel(CH8, output_device, name="DRONE")
arpOut = app.setupOutputChannel(CH9, output_device, name="ARP")
drumOut = app.setupOutputChannel(CH10, output_device, name="DRUMS")

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

# app.patch('Arturia BeatStep_in', 'debug')
app.patch('carpeggio_out', 'debug')

Application.run()
