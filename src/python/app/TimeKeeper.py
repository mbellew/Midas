from datetime import datetime
import mido
from app.Event import Event, EVENT_CLOCK, EVENT_MIDI
from app.MidiMap import MidiMap


class InternalClock:
    """generate 'real' midi clock messages if there is no external source.  This can be used by TimeKeeper
    if there is no external clock"""
    def __init__(self, q, source_name, bpm, ppq=48, sink_name='internal_clock_cc'):
        self.sink = q.createSink('internal_clock_cc', self)
        self.out = q.createSource(source_name)
        self.ppq = ppq
        self.bpm = -1
        self.reset()
        self.update_bpm(bpm)
        self.ccmap = MidiMap()
        self.ccmap.add( 15, lambda m : self.cc_bpm(m))


    def update_bpm(self, bpm):
        if self.bpm == bpm:
            return

        # update start_time, start_pulse so we don't jitter
        self.start_pulse = self.current_pulse
        self.start_time = self.last_time

        self.bpm = bpm
        qps = bpm/60.0
        pps = self.ppq * qps
        self.pulse_length = 1.0 / pps
        print("BPM - " + str(self.bpm))


    def reset(self):
        self.last_time = -1
        self.start_time = -1
        self.current_pulse = 0
        self.start_pulse = 0


    def cc_bpm(self, msg):
        # range 0.5 - 1.0
        r = 0.5 + 0.5*(msg.value/127.0)
        # r*r -> 0.25 - 1.0
        bpm = int(r*r * 240)
        self.update_bpm(bpm)


    def handle(self, event):
        if event.code == EVENT_MIDI:
            msg = event.obj
            if msg.type == 'control_change':
                self.ccmap.dispatch(msg)


    def process(self):
        global MIDI_CLOCK_MESSAGE
        time = datetime.now()
        if self.start_time == -1:
            self.start_time = time
        elapsed = (time - self.start_time)
        pulse = self.start_pulse + int(elapsed.total_seconds()/self.pulse_length)
        if pulse == self.current_pulse:
            return
        if pulse != self.current_pulse+1:
            print('!')
        self.current_pulse = pulse
        self.out.add(Event(EVENT_MIDI, 'internal', mido.Message('clock',time=pulse)))
        return self.current_pulse



class Signature:
    def __init__(self,beats,note,ppq):
        self.note = note
        self.beats = beats
        self.pulses_per_beat = (4*ppq)/note
        self.pulses_per_measure = self.pulses_per_beat * beats



class Pulse:
    """can't really extends mido.Message so use our own internal class"""
    def __init__(self, midi, sig):
        global MIDI_CLOCK_MESSAGE
        self.time  = midi.time                                                  # current pulse since 'start' (zero based)
        self.beat  = int((self.time % sig.pulses_per_measure) / sig.pulses_per_beat)                       # zero-based "0 and 1 and 2 and 3 and"
        self.measure = int(self.time / sig.pulses_per_measure)                     # count of measures since 'start'
        self.pulse   = int(self.time % sig.pulses_per_beat)                          # pulse count in current beat 0-23 
        self.pos     = (self.time % sig.pulses_per_beat) / sig.pulses_per_beat     # progress in current beat 0-1.0 (e.g 1/8 note is 0.5)
 
    def __str__(self):
        return str(vars(self))



class TimeKeeper:
    """This takes a midi clock and generates clock messages with
    beat and measure counts used.  These are the messages used internally by other modules"""
    def __init__(self, q, sink, source, ppq):
        self.sig = Signature(4,4,ppq)
        q.createSink(sink, self)
        self.out = q.createSource(source)
        self.current_pulse = 0


    def handle(self, event):
        # external clock messages probably don't set time
        msg = event.obj
        if msg.type == 'clock':
            msg.time = self.current_pulse
            self.out.add(Event(EVENT_CLOCK, event.source+'/timekeeper', Pulse(msg,self.sig)))
            self.current_pulse = self.current_pulse + 1

        elif msg.type == 'stop':
            self.current_pulse = 0
