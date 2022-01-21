from Application import Application
from midi.MidiServer import *
from midi.Carpeggio import CarpeggioGenerative
from midi.Rhythms import RhythmModule, VolcaBeats, MpcPadsChromaticC1
from midi.ChordySequencer import ChordyModule
from midi.OneNoteSequencer import OneNoteSequencer

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

app.addProgramController('Arturia BeatStep_in', BEATSTEP_CONTROLLER)
app.addProgramController('Midi Fighter Twister_in', TWISTER_CONTROLLER)
# use MidiMix for Ableton app.addProgramController('MIDI Mix_in', AKAIMIDIMIX_CONTROLLER)

DebugModule(q, 'debug')
rm = RhythmModule(q, "rhythm", drumkit=MpcPadsChromaticC1(16))
rm.instrument = [3, 8, 10, 11]
app.addProgram(rm)
bc = BootsNCats(q, "bootsncats", drumkit=MpcPadsChromaticC1(16))
bc.instrument = [0, 1, 2, 3, 6, 12] # kick, kick, snare, clap, 
app.addProgram(ChordyModule(q, "chordy", root=48, minor=False))
OneNoteSequencer(q, "bass", transpose=-12)
OneNoteSequencer(q, "drone")

# 
# Configure OUTPUT channels
#

# TODO app.hasDevice('name')
output_device = 'IAC Driver Bus 1_sink'
bootsOut = app.setupOutputChannel(CH5, output_device, name="BOOTS")
droneOut = app.setupOutputChannel(CH8, output_device, name="DRONE")
arpOut = app.setupOutputChannel(CH9, output_device, name="ARP")
drumOut = app.setupOutputChannel(CH10, output_device, name="DRUMS")
bassOut = app.setupOutputChannel(CH7, output_device, name="BASS")

#
# PATCH!
#

# sequencer needs clock, and supports control_change messages
app.patch('clock', 'rhythm_clock_in')
app.patch('rhythm_out', drumOut)
app.patch('clock', 'bootsncats_clock_in')
app.patch('bootsncats_out', bootsOut)

# sequencer needs clock, and supports control_change messages
app.patch('clock', 'chordy_clock_in')
app.patch("Artiphon Orba MIDI_in", 'chordy_chord_in')
app.patch("Artiphon Orba Bluetooth_in", 'chordy_chord_in')
app.patch('rhythm_trigger1', 'chordy_trigger')
app.patch('chordy_out', arpOut)
#app.patch('chordy_drone', droneOut) # TODO use OneNoteSequencer

# chordy will set the note for bassline
# rhythm will be the trigger
app.patch('chordy_root', 'bass_note_in')
app.patch('rhythm_trigger2', 'bass_trigger')
app.patch('bass_out', bassOut)

app.patch('chordy_root', 'drone_note_in')
app.patch('chordy_root', 'drone_trigger')
app.patch('drone_out', droneOut)


# app.patch('Arturia BeatStep_in', 'debug')
#app.patch(app.getOutputChannel(CH8).output_source, 'debug')
#app.patch(app.getOutputChannel(CH7).output_source, 'debug')
#app.patch(app.getOutputChannel(CH10).output_source, 'debug')
app.patch("Artiphon Orba MIDI_in", 'debug')

Application.run()
