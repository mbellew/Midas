import datetime
import time
import mido
from Event import *
from EventQueue import EventQueue
from TimeKeeper import TimeKeeper
from TransposeModule import TransposeModule




class DebugModule:
    def handle(self, event):
        if event[0] != EVENT_PULSE:
            print(datetime.datetime.now(), event)
        return EVENT_CONTINUE


class MidiOutModule:
    def __init__(self, midiOutputs):
        self.midiOutputs = midiOutputs

    def handle(self, event):
        if EVENT_MIDI_OUT == event[0]:
            p = event[1]
            msg = event[2]

            if p < len(self.midiOutputs):
                self.midiOutputs[p].send(msg)
                return EVENT_DONE
        return EVENT_CONTINUE


class PassthroughModule:
    def __init__(self, midi_in, midi_out, queue=None, port=None):
        self.queue = queue
        self.input_num = midi_in
        self.output_num = midi_out
        self.output_port = port

    def handle(self, event):
        if event[0] != EVENT_MIDI_IN:
            return EVENT_CONTINUE
        source = event[1]
        msg = event[2]
        if source != self.input_num:
            return EVENT_CONTINUE
        # if we have a port send immediately else queue
        if self.output_port:
            self.output_port.send(msg)
        if self.queue:
            self.queue.add((EVENT_MIDI_OUT,self.output_num,msg))
        return


class StrumModule:
    def __init__(self, clock, midi_in, midi_out, queue, minor=False):
        self.queue = queue
        self.clock = clock
        self.input_num = midi_in
        self.output_num = midi_out
        self.minor = minor

    def handle(self, event):
        if event[0] != EVENT_MIDI_IN:
            return EVENT_CONTINUE
        source = event[1]
        msg = event[2]
        if source != self.input_num:
            return EVENT_CONTINUE
        
        if msg.type == 'note_on' or msg.type == 'note_off':
            I = msg.copy(note=msg.note+0)
            III = msg.copy(note=msg.note+(3 if self.minor else 4))
            V = msg.copy(note=msg.note+7)
            VIII = msg.copy(note=msg.note+12)
            speed = 3
            if (msg.type == 'note_off'):
                self.queue.remove_all(lambda e : e[0] == EVENT_MIDI_OUT and e[1] == self.output_num and e[2].type == 'note_on')
                self.queue.add((EVENT_MIDI_OUT, self.output_num, I))
                self.queue.add((EVENT_MIDI_OUT, self.output_num, III))
                self.queue.add((EVENT_MIDI_OUT, self.output_num, V))
                self.queue.add((EVENT_MIDI_OUT, self.output_num, VIII))
            else:
                # find place in measure
                if self.clock.get_time() % 24 < 12:
                    self.queue.delay((EVENT_MIDI_OUT, self.output_num, I),  0*speed)
                    self.queue.delay((EVENT_MIDI_OUT, self.output_num, III),1*speed)
                    self.queue.delay((EVENT_MIDI_OUT, self.output_num, V), 2*speed)
                    self.queue.delay((EVENT_MIDI_OUT, self.output_num, VIII), 3*0*speed)
                else:
                    self.queue.delay((EVENT_MIDI_OUT, self.output_num, VIII),  0*speed)
                    self.queue.delay((EVENT_MIDI_OUT, self.output_num, V),1*speed)
                    self.queue.delay((EVENT_MIDI_OUT, self.output_num, III), 2*speed)
                    self.queue.delay((EVENT_MIDI_OUT, self.output_num, I), 3*0*speed)
        else:
            self.queue.add((EVENT_MIDI_OUT, self.output_num, msg))
        return


class StrumPattern:
    def __init__(self, midi_in, midi_out, queue):
        self.queue = queue
        self.input_num = midi_in
        self.output_num = midi_out
        self.current_msg = None
        if midi_in == midi_out:
            raise


    def handle(self, event):

        if event[0] == EVENT_MIDI_IN:
            source = event[1]
            msg = event[2]
            if source != self.input_num:
                return EVENT_CONTINUE
            if msg.type == 'note_on':
                self.current_msg = msg
            if msg.type == 'note_off':
                if self.current_msg and self.current_msg.note == msg.note:
                    self.current_msg = None
            return EVENT_DONE
        
        if event[0] == EVENT_MEASURE:
            if not self.current_msg or self.current_msg.type != 'note_on':
                return EVENT_CONTINUE            
            msg = self.current_msg
            # send a measure worth of notes            
            self.queue.delay((EVENT_MIDI_IN, self.output_num, msg), 0)  # D
            self.queue.delay((EVENT_MIDI_IN, self.output_num, msg), 24) # D
            self.queue.delay((EVENT_MIDI_IN, self.output_num, msg), 36) # U
            self.queue.delay((EVENT_MIDI_IN, self.output_num, msg), 60) # U
            self.queue.delay((EVENT_MIDI_IN, self.output_num, msg), 72) # D
            self.queue.delay((EVENT_MIDI_IN, self.output_num, msg), 84) # U
            off = mido.Message('note_off', note=msg.note)
            self.queue.delay((EVENT_MIDI_IN, self.output_num, off), 90) # U
        
        return EVENT_CONTINUE 


class Application:

    def __init__(self):        
        self.ppqClock = TimeKeeper(120)
        self.lastPulse = -1
        self.eventQueue = EventQueue(self.ppqClock)
        self.eventHandlers = []
        self.midiInputPorts = []
        self.midiOutputPorts = []
        return


    def process_inputs(self):
        for i in range(0,len(self.midiInputPorts)):
            port = self.midiInputPorts[i]
            for msg in port.iter_pending():
                self.eventQueue.add((EVENT_MIDI_IN,i,msg))
        return


    def update_timers(self):
        pulse = self.ppqClock.update()
        if pulse != self.lastPulse:
            self.eventQueue.add_first((EVENT_PULSE,pulse))
            if 0 == pulse % 24:
                self.eventQueue.add_first((EVENT_TEMPO,pulse,))
            if 0 == pulse % 96:
                self.eventQueue.add_first((EVENT_MEASURE,pulse))
            self.lastPulse = pulse
        return


    def process_events(self):
        event = self.eventQueue.get()
        while event:
            # fake loop to break out of (does python have named blocked?)
            while True:
                for eventHandler in self.eventHandlers:
                    ret = eventHandler.handle(event)
                    if ret == EVENT_DONE:
                        break
                break
            event = self.eventQueue.get()
        return


    def setup(self):
        self.midiInputPorts.append(mido.open_input(mido.get_input_names()[1]))  // mio:
        self.midiInputPorts.append(mido.open_input(mido.get_input_names()[2]))   // Midi Fighter Twister
        self.midiInputPorts.append(mido.open_input(mido.get_input_names()[3]))  // Lauchpad Mini:
        self.midiOutputPorts.append(mido.open_output(mido.get_output_names()[1]))

        self.eventHandlers.append(DebugModule())
        self.eventHandlers.append(MidiOutModule(self.midiOutputPorts))
        #self.eventHandlers.append(PassthroughModule(0,0,port=self.midiOutputPorts[0]))
        #self.eventHandlers.append(PassthroughModule(0,0,queue=self.eventQueue))
        #self.eventHandlers.append(TransposeModule(1,0,100,self.eventQueue))
        
        self.eventHandlers.append(StrumPattern(0, 100, queue=self.eventQueue))

        self.eventHandlers.append(StrumModule(self.ppqClock, 100, 0, queue=self.eventQueue))

        self.eventHandlers.append(TransposeModule(1,101,0,self.eventQueue))

        self.ppqClock.reset()
        return


    def loop(self):
        self.process_inputs()
        self.update_timers()
        self.process_events()
        time.sleep(0.001)
        return


    def main(self):
        self.setup()
        while True:
            self.loop()
        return


print(mido.get_input_names())

application = Application()
application.main()

# print(mido.get_input_names())
# print(mido.get_output_names())
# default_input = mido.open_input(mido.get_input_names()[1])
# print(default_input.name)
# default_output = mido.open_output(mido.get_output_names()[1])
# print(default_output.name)

# for message in default_input:
#     default_output.send(message)
