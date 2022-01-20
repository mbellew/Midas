from midi.Module import AbstractModule
from midi.Event import EVENT_MIDI, Event
from midi.Chords import Chord, find_chord
from random import random, randrange
from midi.GlobalState import GlobalState
import mido

#
# This module basically does... nothing.
# You need to hook up a 
#   1) trigger mechanism (when notes are played)
#   2) set of notes available to be played (e.g. major scale, or pentatonic scale, or a chord)
#   2) arpeggiator (note chooser) and a 
#
# The class Sequencer can be subclassed to pre-patch default behavior
#
# By default all notes from previous trigger are turned off by subsequent trigger.
# Do we need custom note-length behavior?
#

# base class for generative sequences

class Sequencer(AbstractModule):
    def __init__(self, q, name):
        # sub-class might have default behavior for firing trigger()
        # TODO probably need to be able to tell if trigger input is patched.
        self.name = name
        q.createSink(name + "_trigger", self.handle_trigger)
        q.createSink(name + "_clock_in", self.handle)
        self.out = q.createSource(name + "_out")
        self.notes = Chord(find_chord("Penta"),36).generate_sequence(10)
        self.listen_for_external_trigger = True
        self.external_trigger_seen = False  # TODO this is a hack
        self.notes_played = []
        self.legato = False
        self.ppq = GlobalState.PPQ
        self.last_trigger = -1


    def handle_clock(self, pulse):
        if not pulse.sixteenth:
            return
        time = pulse.time
        # every sixteenth check if there are notes to turn off
        stop_list = []
        for i in range(len(self.notes_played)-1, -1, -1):
            if self.notes_played[i][1] <= time:
                stop_list.append(self.notes_played[i])
                self.notes_played.pop(i)
        self.stop_notes(stop_list)


    def stop_notes(self, note_pairs):
        for note_on in note_pairs:
            note_off = note_on[0].copy(velocity=0)
            self.out.add(Event(EVENT_MIDI, self.name, note_off))


    def handle_stop(self):
        self.stop_notes(self.notes_played)
        self.notes_played = []


    def handle_trigger(self, event):
        # listen for any note_on
        if self.listen_for_external_trigger and event.code == EVENT_MIDI and event.obj.type == 'note_on':
            self.external_trigger_seen = True
            self.trigger()


    def trigger(self):
        pulse = GlobalState.pulse
        # ignore duplicate trigger on same pulse
        if self.last_trigger == pulse.time:
            return
        self.last_trigger = pulse.time

        notes_played = self.notes_played
        self.notes_played = []
        if not self.legato:
            self.stop_notes(notes_played)
        
        notes = self.play_notes()
        for note_pair in notes:
            note = note_pair[0]
            duration = note_pair[1]
            note.time = pulse.time
            self.notes_played.append( (note, pulse.time + duration*self.ppq) )
            self.out.add(Event(EVENT_MIDI, self.name, note))

        if self.legato:
            self.stop_notes(notes_played)


    def set_notes(self, notes):
        self.notes = notes


    # return an array of notes to turn on and note length
    # [(mido.Message(C3), 1), (mido.Message(F2), 1)]
    # regardless of length, all notes will be turned off with next trigger (or stop)
    def play_notes(self):
        r = randrange(0, len(self.notes))
        message = mido.Message('note_on', self.notes[r])
        return [(message, 1)]