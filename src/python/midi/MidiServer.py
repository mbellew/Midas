import asyncio
import datetime
import signal
import threading

from midi.DisplayArea import DisplayArea
from midi.GlobalState import GlobalState
from midi.Module import AbstractModule
from midi.PatchQueue import PatchQueue, SINK_POINT, SOURCE_POINT
from midi.Rhythms import *
from midi.TimeKeeper import TimeKeeper, InternalClock
from www.HttpServer import HttpServer

# I think this is most common
PPQ = 24

# channels are 0 based which is confusing, here are some constants
(CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9,CH10,CH11,CH12,CH13,CH14,CH15,CH16) = range(0,16)

BEATSTEP_CONTROLLER = "BEATSTEP"
TWISTER_CONTROLLER = "TWISTER"
AKAIMIDIMIX_CONTROLLER = "AKAIMIDIMIX"


__unique__ = 100


def make_mido_stream():
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    def callback(message):
        loop.call_soon_threadsafe(queue.put_nowait, message)
    async def stream():
        while True:
            yield await queue.get()
    return callback, stream()


def unique_name(s):
    global __unique__
    __unique__ = __unique__ + 1
    return str(s) + str(__unique__)


class DebugModule:
    def __init__(self, q, sinkName,):
        q.createSink(sinkName, self.handle)

    def handle(self, event):
        #if EVENT_CLOCK == event.code and event.obj.pulse > 0:
        #    return
        print(datetime.datetime.now(), ' ', event.source, ' ', event.obj)
        return EVENT_CONTINUE


class DebugSendNotes:
    def __init__(self, q, sink, source):
        q.createSink(sink, self)
        self.out = q.createSource(source)

    def handle(self, event):
        if EVENT_CLOCK == event.code and 0==event.obj.pulse:
            self.out.add(Event(EVENT_MIDI,'debug',mido.Message('note_on',note=60)))
            self.out.delay(Event(EVENT_MIDI,'debug',mido.Message('note_off',note=60)),12)


class MidiInputStep:
    def __init__(self, q, port_name, point, clock=None):
        # self.port = mido.open_input(port_name, callback=lambda m : self.on_message(m))
        self.q = q
        self.port = mido.open_input(port_name)
        self.point = q.createSource(point)
        self.clock = None if clock is None else q.createSource(clock)    
        self.is_patched = None

    def process(self):
        if self.is_patched is None:
            self.is_patched = self.q.isPatched(self.point) or self.q.isPatched(self.clock)
        if not self.is_patched:
            return False
        new_events = False
        if self.port:
            for msg in self.port.iter_pending():
                self.on_message(msg)
                new_events = True
        return new_events

    def on_message(self,msg):
        if msg.type=='aftertouch':
            return
        if self.clock and (msg.type == 'clock' or msg.type == 'stop' or msg.type == 'songpos' or msg.type == 'continue'):
            self.clock.add(Event(EVENT_MIDI,self.port.name,msg))
        else:
            self.point.add(Event(EVENT_MIDI,self.port.name,msg))


class MidiOutModule(AbstractModule):
    def __init__(self, q, sink, port):
        super().__init__()
        q.createSink(sink, self)
        self.port = port

    def handle_note(self, msg):
        if self.port:
            self.port.send(msg)

    def handle_clock(self, pulse):
        self.handle_note(pulse.msg)


class MidiChannelFilter:
    def __init__(self,q,in_channel=None,out_channel=-1,sink_name=None,source_name=None):
        global patch_point_unique
        if not sink_name:
            sink_name = unique_name("MidiChannelFilter_sink_")
        self.sink = q.createSink(sink_name, self.handle)
        if not source_name:
            source_name = unique_name("MidiChannelFilter_source_")
        self.sink_name = sink_name
        self.source_name = source_name
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
        if msg.channel is None:
            return
        if self.in_channel is not None and msg.channel != self.in_channel:
            return
        out_msg = msg
        if out_msg.channel != self.out_channel:
            out_msg = out_msg.copy(channel=self.out_channel)
        self.source.add(Event(EVENT_MIDI, event.source+"/"+self.name, out_msg))


class PassthroughModule:
    def __init__(self, q, source_name, sink_name=None):
        if not sink_name:
            sink_name = unique_name("passthrough_")
        self.sink = q.createSink(sink_name, self.handle)
        self.source_name = source_name
        self.output_point = q.createSource(self.source_name)
        self.isPassthroughModule = True

    def handle(self, event):
        if EVENT_MIDI != event.code:
            return
        msg = event.obj
        if self.output_point:
            self.output_point.add(Event(EVENT_MIDI, self.output_point.name, msg))
        return


# this is not a module, it is a helper that setup up patches
# TODO keep track of created patches/MidiChannelFilter so the OutputChannel can be modified 
class OutputChannel:
    def __init__(self, q, channel):
        self.q = q
        self.channel = channel
        self.target_name = None
        self.target_midi_channel = channel
        self.output_source = None
        self.passthrough = None
        self.midifilter = None
        self.sink_name = "CH" + str(channel+1)
        self.source_name = None
        self.name = self.sink_name
        q.createSink(self.sink_name)

    def setup(self, device, channel=None, name=None):
        if channel is not None:
            self.channel = channel
        if name:
            self.name = name
        self.midifilter = MidiChannelFilter(self.q, None, self.channel, self.sink_name)
        self.q.createPatch(self.midifilter.source_name, device)  
        self.output_source = self.midifilter.source_name



class ProgramController:
    def __init__(self, app):
        self.app = app
        self.shifted = False

    # normalize to shift/pg next/pg prev/knobs=0-15/pads=16-31
    def remap(self, msg):
        return msg

    def shift(self, shifted):
        self.shifted = shifted
        return None

    def program_next(self):
        self.app.current_program = (self.app.current_program + 1) % len(self.app.programs)
        self.app.current_program_sink = self.app.programs[self.app.current_program].get_control_sink()
        self.app.repaint = True
        return None

    def program_prev(self):
        self.app.current_program = (self.app.current_program + len(self.app.programs) - 1) % len(self.app.programs)
        self.app.current_program_sink = self.app.programs[self.app.current_program].get_control_sink()
        self.app.repaint = True
        return None

    def handle(self, event):
        if event.code != EVENT_MIDI or len(self.app.programs) == 0:
            return

        msg = self.remap(event.obj)
        if not msg:
            return
        program_change = None

        pad = None
        # ASSUME PADS ARE (channel=2 control=0-15) or (channel=* control 16-31)
        if msg.type == 'control_change' and (16 <= msg.control < 32):
            pad = msg.control % 16

        if msg.type == 'program_change':
            program_change = msg.program
        elif self.shifted and pad is not None:
            program_change = pad
        if program_change is not None and program_change < len(self.app.programs):
            if self.app.current_program != program_change:
                self.app.current_program = program_change
                self.app.current_program_sink = self.app.programs[self.app.current_program].get_control_sink()
                self.app.repaint = True
        elif msg.type == 'control_change':
            if self.app.current_program_sink:
                self.app.current_program_sink.add(Event(EVENT_MIDI, event.source, msg))
        return


class AkaiMidiMix(ProgramController):
    def __init__(self, app):
        super().__init__(app)

    def remap(self, msg):
        # KNOBS
        if msg.type == 'control_change':
            if msg.control >= 16:
                control = msg.control-30 if msg.control >= 46 else msg.control-16
                col = int(control / 4)
                row = int(control % 4)
                # ignore rows 3 and 4
                if row > 1 or col > 7:
                    return None
                return msg.copy(control=row * 8 + col)
            # BUTTONS
        elif msg.type == 'note_on' or msg.type == 'note_off':
            if msg.note == 25:
                return None if msg.type == 'note_off' else self.program_next()
            elif msg.note == 26:
                return None if msg.type == 'note_off' else self.program_prev()
            elif msg.note == 27:
                return self.shift(msg.type=='note_on')
            elif msg.note >= 1:
                note = msg.note-1
                col = int(note / 3)
                row = note % 3
                if row > 3 or col > 7:
                    return None
                # row 0 shifts to row 1, row 2 does not shift
                control = 16 + col if row < 2 else 24 + col
                value = 0 if msg.type == 'note_off' else 127
                return mido.Message('control_change', control=control, value=value)
        return None


class BeatStepCustomMap(ProgramController):
    def __init__(self, app):
        super().__init__(app)

    def remap(self, msg):
        if msg.type == 'control_change':
            if msg.channel == CH16:
                # can't seem to change msg.control on BEATSTEP/STOP (always 1), but I can set channel to CH16
                if msg.control == 1 or msg.control == 127:
                    return self.shift(msg.value == 127)
                return None
            elif msg.control == 100 and (msg.value == 1 or msg.value == 127):
                if msg.value == 127:
                    return self.program_prev()
                else:
                    return self.program_next()
            elif msg.control >= 16:
                return msg.copy(control = (msg.control % 16) + 16)
        return msg


class FighterTwister(ProgramController):
    def __init__(self, app):
        super().__init__(app)

    def remap(self, msg):
        # TWISTER
        if msg.type == 'control_change':
            if msg.channel == CH4:
                # left-top side button
                if msg.control == 8:
                    return self.shift(msg.value == 127)
                return None
            if msg.channel == CH2:
                return msg.copy(control = (msg.control % 16) + 16)
        return msg





class MidiServer:

    def __init__(self):
        global PPQ
        GlobalState.PPQ = PPQ
        self.webserver = None
        self.screen = DisplayArea.screen(25, 80)
        self.screen.dirty = True
        self.lastPulse = -1
        self.patchQueue = PatchQueue('queue_clock_in')
        q = self.patchQueue
        self.steps = []
        self.output_channels = []
        for ch in range(0,16):
            self.output_channels.append(OutputChannel(q,ch))

        # for controller patching and UI rendering
        self.programs = []
        self.current_program = 0
        self.current_program_sink = None
        self.controller_sink = {
            BEATSTEP_CONTROLLER: self.sink("controller_bs_sink", BeatStepCustomMap(self).handle),
            TWISTER_CONTROLLER: self.sink("controller_tw_sink", FighterTwister(self).handle),
            AKAIMIDIMIX_CONTROLLER: self.sink("controller_mm_sink", AkaiMidiMix(self).handle)}

        self.displayprops = {'current_program':-1, 'bpm':-1}

        #
        # Wire up the CLOCK and QUEUE
        #

        self.internal_clock = None
        self.timeKeeper = TimeKeeper( self.patchQueue, 'timekeeper_in', 'clock', PPQ)
        self.steps.append( self.patchQueue )
        self.patch('clock', 'queue_clock_in')

        self.findMidiInputs()
        self.findMidiOutputs()
        return None


    def getOutputChannel(self, ch):
        return self.output_channels[ch]


    def setupOutputChannel(self, ch, device, channel=None, name=None):
        self.output_channels[ch].setup(device, channel, name)
        return self.output_channels[ch].sink_name


    def addProgram(self, module):
        # fail fast, see if this is a program module
        if not module.isProgramModule():
            raise Exception("bad config")
        p = len(self.programs)
        module.set_display_area(self.screen.subArea(p*8+2, 8, 7, 40))
        module.update_display()
        self.programs.append(module)
        if p == self.current_program:
            self.current_program_sink = self.programs[p].get_control_sink()
        pass

    
    def useInternalClock(self, bpm=90):
        self.internal_clock = InternalClock(self.patchQueue, 'internal_clock', bpm, PPQ)
        self.patch('internal_clock','timekeeper_in')
        self.steps.insert(0, self.internal_clock)
        # TODO self.patch('knobs','internal_clock_cc')


    def useExternalClock(self, source):
        self.patch(source, 'timekeeper_in')


    def update_display(self,repaint=False):
        #TODO check if current_program or bpm have changed
        bpm = "ext"
        if self.internal_clock:
            bpm = str(self.internal_clock.bpm)
        if bpm != self.displayprops['bpm']:
            self.screen.right(0,75,bpm)
            self.displayprops['bpm'] = bpm
        if self.current_program != self.displayprops['current_program']:
            self.displayprops['current_program'] = self.current_program
            for i in range(0,len(self.programs)):
                row = i*8+1
                self.screen.right(row,1,str(i),pad=2)
                self.screen.write(row,4,self.programs[i].get_display_name())
                if i==self.current_program:
                    for r in range(row,row+7):
                        self.screen.write(r,0,'|',eol=False)
                else:
                    for r in range(row,row+7):
                        self.screen.write(r,0,' ',eol=False)


    async def render_display(self, force=False):
        if not force and not self.screen.isDirty():
            return
        s = self.screen.toString()
        print("------------------------")
        print(s)
        print("------------------------")
        if GlobalState.webserver:
            await GlobalState.webserver.update(s)


    def addProgramController(self, source, type):
        sink = self.controller_sink[type]
        if sink:
            self.patch(source, sink)


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
        elif type(device) == int:
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
            # skip twister if I'm using it for MPC
            #if name.startswith("Midi Fighter Twister"):
            #    continue
            try:
                step = MidiInputStep(q, name, name + "_in", name + "_clock")
                # We don't need to do this if MidiInputStep uses callback
                self.steps.append(step)
            except:
                print("ERROR: failed to open port '" + name + "'")
                continue

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
            ptm = PassthroughModule(q, "keyboard", "passthrough_keyboard")
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
            try:
                MidiOutModule(q, name + "_sink", mido.open_output(name))
            except Exception as ex:
                print("ERROR: failed to open port '" + name + "'")
                print(ex)
                continue

        instrumentName = None
        if not instrumentName:
            for n in names:
                if n.startswith("IAC Driver Bus 1"):
                    instrumentName = n
                    break

        if not instrumentName:
            for n in names:
                if n.startswith("Arturia MicroFreak"):
                    instrumentName = n
                    break

        if not instrumentName:
            for n in names:
                if n.startswith("Scarlett 4i4 USB"):
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


    def patch_set(self):
        raise Exception("YOU NEED TO IMPLEMENT THIS")


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


    async def loop(self):
        try:
            did_something = False
            for step in self.steps:
                result = step.process()
                if result:
                    did_something = True
            if not did_something:
                self.update_display()
                await self.render_display()
            await asyncio.sleep(0.005 if did_something else 0.001)
        finally:
            pass


    async def loop_forever(self):
        try:
            self.print_patch()
            self.patchQueue.optimize()
            while not GlobalState.stop_event.is_set():
                await self.loop()
        except Exception as ex:
            print("loop_forever()", ex)
        finally:
            print("MidiServer.loop_forever() is done is_set()==" + str(GlobalState.stop_event.is_set()))


    def stop(self):
        self.timeKeeper.stop()
