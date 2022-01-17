from Application import Application
from midi.MidiServer import *
from midi.Carpeggio import CarpeggioGenerative
from midi.Rhythms import RhythmModule, VolcaBeats, MpcPadsChromaticC1

app = Application.create()
q = app.patchQueue

#
# CLOCK
#

app.useExternalClock('IAC Driver Bus 1_clock')
# app.useInternalClock(120)


#
# MODULES
#

# Create the modules we want to use
# "Programs" are modules that have CC control and/or show up in the 'UI'
# TODO have addProgram() wire up clock_in and ppq

app.addProgramController('Arturia BeatStep_in', BEATSTEP_CONTROLLER)
app.addProgramController('Midi Fighter Twister_in', TWISTER_CONTROLLER)
# use MidiMix for Ableton app.addProgramController('MIDI Mix_in', AKAIMIDIMIX_CONTROLLER)

DebugModule(q, 'debug')
rm = RhythmModule(q, "rhythm", drumkit=MpcPadsChromaticC1(16), ppq=PPQ)
rm.instrument = [3, 8, 10, 11]
app.addProgram(rm)
bc = BootsNCats(q, "bootsncats", drumkit=MpcPadsChromaticC1(16), ppq=PPQ)
bc.instrument = [0, 1, 2, 3, 6, 12] # kick, kick, snare, clap, 
app.addProgram(CarpeggioGenerative(q, "carpeggio", ppq=PPQ, root=48, minor=True))
   

# 
# Configure OUTPUT channels
#

# TODO app.hasDevice('name')
output_device = 'IAC Driver Bus 1_sink'
bootsOut = app.setupOutputChannel(CH5, output_device, name="BOOTS")
droneOut = app.setupOutputChannel(CH8, output_device, name="DRONE")
arpOut = app.setupOutputChannel(CH9, output_device, name="ARP")
drumOut = app.setupOutputChannel(CH10, output_device, name="DRUMS")

#
# PATCH!
#

# sequencer needs clock, and supports control_change messages
app.patch('clock', 'rhythm_clock_in')
app.patch('rhythm_out', drumOut)
app.patch('clock', 'bootsncats_clock_in')
app.patch('bootsncats_out', bootsOut)

# sequencer needs clock, and supports control_change messages
app.patch('clock', 'carpeggio_clock_in')
app.patch('Scarlett 4i4 USB_in', 'carpeggio_chord_in')
app.patch('carpeggio_out', arpOut)
app.patch('carpeggio_drone', droneOut)   

# app.patch('Arturia BeatStep_in', 'debug')
app.patch(app.getOutputChannel(CH8).output_source, 'debug')
app.patch(app.getOutputChannel(CH9).output_source, 'debug')
app.patch(app.getOutputChannel(CH10).output_source, 'debug')
app.patch("rhythm_trigger1", 'debug')

Application.run()
