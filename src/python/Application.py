import datetime
import time
import mido
from Event import *
from PatchQueue import PatchQueue, SINK_POINT, SOURCE_POINT
from TimeKeeper import TimeKeeper, InternalClock
from TransposeModule import TransposeModule
from StrumArpeggiator import StrumArpeggiator
from StrumPattern import StrumPattern
from Rhythms import *


__unique__ = 100

def unique_name(s):
    global __unique__
    __unique__ = __unique__ + 1
    return str(s) + str(__unique__)


# class TimerStep:
#     def __init__(self, clock, point):
#         self.last_pulse = -1
#         self.clock = clock
#         self.point = point
#         self.clock.reset()

#     def process(self):
#         pulse = self.clock.update()
#         if pulse == self.last_pulse:
#             return False
#         self.point.add_first((EVENT_PULSE,pulse))
#         if 0 == pulse % 24:
#             self.point.add_first((EVENT_TEMPO,pulse))
#         if 0 == pulse % 96:
#             self.point.add_first((EVENT_MEASURE,pulse))
#         self.last_pulse = pulse
#         return True



class DebugModule:
    def __init__(self, q, sinkName,):
        q.createSink(sinkName, self)

    def handle(self, event):
        if EVENT_CLOCK == event.code and event.obj.pulse > 0:
            return
        print(datetime.datetime.now(), event)
        return EVENT_CONTINUE


class DebugNotes:
    def __init__(self, q, sink, source):
        q.createSink(sink, self)
        self.out = q.createSource(source)

    def handle(self, event):
        if EVENT_CLOCK == event.code and 0==event.obj.pulse:
            self.out.add(Event(EVENT_MIDI,'debug',mido.Message('note_on',note=60)))
            self.out.delay(Event(EVENT_MIDI,'debug',mido.Message('note_off',note=60)),12)


class MidiInputStep:
    def __init__(self, q, point, port, clock=None):
        self.port = port
        self.point = q.createSource(point)
        self.clock = None if clock is None else q.createSource(clock)
    

    def process(self):
        new_events = False
        if self.port:
            for msg in self.port.iter_pending():
                if msg.type=='aftertouch':
                    continue
                if msg.type == 'clock':
                    if self.clock:
                        self.clock.add(Event(EVENT_MIDI,self.port.name,msg))
                else:
                    self.point.add(Event(EVENT_MIDI,self.port.name,msg))
                new_events = True
        return new_events



class MidiOutModule:
    def __init__(self, q, sink, port):
        q.createSink(sink, self)
        self.port = port

    def handle(self, event):
        if EVENT_MIDI != event.code:
            return
        msg = event.obj
        if self.port:
            self.port.send(msg)
        return EVENT_DONE



class MidiChannelFilter:
    def __init__(self,q,in_channel,out_channel=-1,sink_name=None,source_name=None):
        global patch_point_unique
        if not sink_name:
            sink_name = unique_name("MidiChannelFilter_sink_")
        self.sink = q.createSink(sink_name, self)
        if not source_name:
            source_name = unique_name("MidiChannelFilter_source_")
        self.source = q.createSource(source_name)
        self.in_channel = in_channel
        self.out_channel = in_channel if out_channel == -1 else out_channel
        self.name = "midi(" + str(self.in_channel) + "-> " + str(self.out_channel) + ")"

    def handle(self, event):
        if EVENT_MIDI != event.code:
            return
        msg = event.obj
        if msg.type != 'note_on' and msg.type != 'note_off':
            return
        if not msg.channel or msg.channel != self.in_channel:
            return
        out_msg = msg.copy(channel=self.out_channel)
        self.source.add(Event(EVENT_MIDI, event.source+"/"+self.name,out_msg));



class PassthroughModule:
    def __init__(self, q, source_name, sink_name=None):
        if not sink_name:
            sink_name = unique_name("passthrough_")
        self.sink = q.createSink(sink_name, self)
        self.output_point = q.createSource(source_name)

    def handle(self, event):
        if EVENT_MIDI != event.code:
            return
        msg = event.obj
        if self.output_point:
            self.output_point.add(Event(EVENT_MIDI, self.output_point.name, msg))
        return



class Application:

    def __init__(self):
        self.lastPulse = -1
        self.patchQueue = PatchQueue('queue_clock_in')
        self.steps = []
        return None


    def process_events(self):
        while self.patchQueue.process():
            pass
        return None


    def source(self, name):
        p = self.patchQueue.createPoint(name, SOURCE_POINT)
        return p


    def sink(self, name, handler=None):
        p = self.patchQueue.createPoint(name, SINK_POINT, handler)
        return p


    def patch(self, src, dst):
        self.patchQueue.createPatch(src, dst)
        return None


    def patchChannel(self, src, dst, in_channel, out_channel=-1):
        m = MidiChannelFilter(self.patchQueue, in_channel, out_channel)
        self.patchQueue.createPatch(src, m.sink)
        self.patchQueue.createPatch(m.source, dst)
        return None


    def open_midi_sink(self, device):
        if type(device) == type(''):
            for name in mido.get_input_names():
                if name.startswith(device):
                    device = name
                    break
        elif type(device) == type(1):
            device = mido.get_input_names()[device]
        port = mido.open_output(device)
        return MidiOutModule(port)



    def findMidiInputs(self):
        q = self.patchQueue
        names_list = mido.get_input_names()

        # mido.get_input_names() returns duplicates!  so remove them
        names = {}
        for name in names_list:
            names[name] = name
        
        # create a source for every input
        for name in names:
            step = MidiInputStep(q, name + "_in", mido.open_input(name))
            self.steps.append(step)

        # create "keyboard" source

        keyboardName = None
        for n in names:
            if n.startswith("Arturia KeyStep"):
                keyboardName = n
                break
        
        if not keyboardName: 
            for n in names:
                if n.startswith("mio:") or n=="mio":
                    keyboardName = n
                    break

        self.patchQueue.createSource("keyboard")
        if keyboardName:
            # TODO create aliases for sources to avoid needing to create new sinks and patches
            print("opening '" + keyboardName + "' as 'keyboard'")
            ptm = PassthroughModule(q, "keyboard", "passthrogh_keyboard")
            self.patch(keyboardName + "_in", ptm.sink)

        # look for fighter twister

        twisterDevice = None
        for n in names:
            if n.startswith("Midi Fighter Twister"):
                twisterDevice = n
        self.patchQueue.createSource("knobs")
        if twisterDevice:
            print("opening '" + twisterDevice + "' as 'knobs'")
            ptm = PassthroughModule(q, "knobs", "passthrough_knobs")
            self.patch(twisterDevice + "_in", ptm.sink)

        # look for novation lauchpad 

        launchpadDevice = None
        for n in names:
            if n.startswith("Launchpad"):
                launchpadDevice = n
        self.patchQueue.createSource("grid")
        if launchpadDevice:
            print("opening '" + launchpadDevice + "' as 'grid'")
            ptm = PassthroughModule(q, "grid", "passthrough_grid")
            self.patch(launchpadDevice + "_source", ptm.sink)


    def findMidiOutputs(self):
        q = self.patchQueue
        names_list = mido.get_input_names()
        print(names_list)

        # mido.get_input_names() returns duplicates!  so remove them
        names = {}
        for name in names_list:
            names[name] = name

        # create a sink for every output
        for name in names:
            MidiOutModule(q, name + "_sink", mido.open_output(name))

        instrumentName = None
        if not instrumentName:
            for n in names:
                if n.startswith("Arturia MicroFreak"):
                    instrumentName = n
                    break
        if not instrumentName:
            for n in names:
                if n.startswith("mio:") or n=="mio":
                    instrumentName = n
                    break

        # create output handler for midi0
        self.sink('instrument', None)
        if instrumentName: 
            print("opening '" + instrumentName + "' as 'instrument'")
            MidiOutModule(q, 'instrument', mido.open_output(instrumentName))


    def setup(self):
        q = self.patchQueue

        #
        # Wire up the CLOCK and QUEUE
        #

        self.steps.append( InternalClock(q, 'internal_clock', 180) )
        TimeKeeper(q, 'timekeeper_in', 'clock')
        self.steps.append( self.patchQueue )
        self.patch('clock', 'queue_clock_in')

        #
        # MIDI DEVICES
        #

        # keyboard, knobs, grid
        self.findMidiInputs()

        # instrument
        self.findMidiOutputs()

        #
        # MODULES
        #

        StrumArpeggiator(q, 'arp_in', 'arp_out')
        StrumPattern(q, 'strumpattern_in', 'strumpattern_out')
        DebugModule(q, 'debug')
        DebugNotes(q, 'debug_notes_in', 'debug_notes_out')
        TransposeModule(q, 'transpose_cc', 'transpose_notes', 'transpose_out')
        RhythmModule(q, "rhythm_clock_in", "rhythm_cc_in", "rhythm_beat_out", PASHTO)
    
        # 
        # PATCH!
        #

        # USE THIS IF THERE IS NO EXTERNAL MIDI CLOCK
        self.patch('internal_clock', 'timekeeper_in')
        #self.patch('keyboard','timekeeper_in')

        self.patch('clock','rhythm_clock_in')
        self.patch('knobs','rhythm_cc_in')
        self.patch('rhythm_beat_out','instrument')
        #self.patch('keyboard','instrument')

	# debugging
        #self.patch('grid', 'debug')
        #self.patch('knobs', 'debug')
        #self.patch('Rhythm_out', 'debug')
        #self.patch('arp_out', 'debug')
        self.patch('clock','debug')

        # GO!

        #self.ppqClock.reset()

        return


    def print_patch(self):
        print("")
        print("patch sources")
        self.patchQueue.printSources()
        print("")
        print("patch sinks")
        self.patchQueue.printSinks()
        print("")
        print("patch connections")
        self.patchQueue.printPatches()
        print("")


    def loop(self):
        didsomething = False
        for step in self.steps:
            result = step.process()
            if result: didsomething = True
        if not didsomething:
            time.sleep(0.001)
        return


    def main(self):
        self.setup()
        self.print_patch()
        self.patchQueue.optimize()
        while True:
            self.loop()
        return


#print("SOURCES")
#for name in mido.get_input_names():
#    print("  ", name)
#print("SINKS")
#for name in mido.get_output_names():
#    print("  ", name)


application = Application()
application.main()

