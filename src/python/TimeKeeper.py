from datetime import datetime
import mido
from Event import Event, EVENT_CLOCK, EVENT_MIDI


class InternalClock:
    """generate 'real' midi clock messages if there is no external source.  This can be used by TimeKeeper
    if there is no external clock"""
    def __init__(self, q, source_name, bpm):
        self.out = q.createSource(source_name)
        self.bpm = bpm
        self.start_time = -1
        self.current_pulse = -1
        self.ppq = 24
        pps = float(bpm)*self.ppq/60.0
        self.pulse_length = 1.0 / pps
        
    def reset(self):
        self.start_time = -1
        self.current_pulse = -1

    def process(self):
        global MIDI_CLOCK_MESSAGE
        time = datetime.now()
        if self.start_time == -1:
            self.start_time = time
        elapsed = (time - self.start_time)
        pulse = int(elapsed.total_seconds()/self.pulse_length)
        if pulse != self.current_pulse:
            self.current_pulse = pulse
            self.out.add(Event(EVENT_MIDI, 'internal', mido.Message('clock',time=pulse)))
        return self.current_pulse



class Signature:
    def __init__(self,beats,note):
        self.note = note
        self.beats = beats
        self.pulses_per_beat = (4*24)/note
        self.pulses_per_measure = self.pulses_per_beat * beats

TWOFOUR = Signature(2,4)
THREEFOUR = Signature(3,4)
FOURFOUR = Signature(4,4)



class Pulse:
    """can't really extends mido.Message so use our own internal class"""
    def __init__(self, midi, sig):
        global MIDI_CLOCK_MESSAGE
        self.time  = midi.time                                                  # current pulse since 'start' (zero based)
        self.beat  = (int)((self.time % sig.pulses_per_measure) / sig.pulses_per_beat)                       # zero-based "0 and 1 and 2 and 3 and"
        self.measure = (int)(self.time / sig.pulses_per_measure)                     # count of measures since 'start'
        self.pulse   = self.time % sig.pulses_per_beat                          # pulse count in current beat 0-23 
        self.pos     = (self.time % sig.pulses_per_beat) / sig.pulses_per_beat     # progress in current beat 0-1.0 (e.g 1/8 note is 0.5)
 
    def __str__(self):
        return str(vars(self))



class TimeKeeper:
    """This takes a midi clock and generates clock messages with
    beat and measure counts used.  These are the messages used internally by other modules"""
    def __init__(self, q, sink, source, sig=None):
        self.sig = sig or FOURFOUR
        q.createSink(sink, self)
        self.out = q.createSource(source)


    def handle(self, event):
        self.out.add(Event(EVENT_CLOCK, event.source+'/timekeeper', Pulse(event.obj,self.sig)))