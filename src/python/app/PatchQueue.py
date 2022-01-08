from app.DelayQueue import DelayQueue
from app.Event import EVENT_CLOCK

# we want to act more or less single threaded, dispatchEvent is a good choke-point
# from threading import RLock
# _THREAD_LOCK_ = RLock()
_THREAD_LOCK_ = None

SINK_POINT = 100
SOURCE_POINT = 201


class Point:
    def __init__(self, queue, name, inout, handler):
        self.parent = queue
        self.name = name
        self.inout = inout
        self.handler = handler

    def add(self, event):
        self.parent.dispatchEvent(event, self)

    def add_first(self, event):
        self.parent.add_first(event, self)

    def delay(self, event, delay):
        self.parent.delay(event, delay, self)

    def remove_all(self, fn):
        self.parent.remove_all(fn, self)


class PatchQueueEvent:
    def __init__(self, event, point):
        self.event = event
        self.point = point


class PatchQueue:
    def __init__(self, clock_sink):
        self.stringType = type('')
        self.listType = type((0,1))
        self.points = {}
        self.patches = {}
        self.createSink(clock_sink,self)
        self.queue = DelayQueue()


    def handle(self, event):
        if EVENT_CLOCK == event.code:
            self.queue.set_time(event.obj.time)


    def createSink(self, sink, handler=None):
        return self.createPoint(sink, SINK_POINT, handler)


    def createSource(self, sourceName):
        return self.createPoint(sourceName, SOURCE_POINT)


    def createPoint(self, sink, inout, handler=None):
        if type(sink) == self.stringType:
            name = sink            
            if not name in self.points:
                point = Point(self, name, inout, handler)
                self.points[name] = point
                return point
            else:
                point = self.points[name]
                if point.inout != inout:
                    raise BaseException("ERROR")
                if handler:
                    if point.handler:
                        raise 
                    point.handler = handler
                return point
        else:
            if sink != self.points[sink.name]:
                raise BaseException()
            if not sink.handler:
                sink.handler = handler
            return sink


    def getPoint(self, name):
        if not name in self.points:
            raise
        return self.points[name]


    def optimize(self):
        for i in range(0,20):
            if not self.optimize_pass():
                return

    def optimize_pass(self):
        # for each source if it only has one patch, and that patch has a handler, then short-circuit
        changed = 0
        for source_name in self.points:
            source = self.points[source_name]
            if source.inout != SOURCE_POINT:
                continue
            if source.handler or not source_name in self.patches:
                continue
            patch_sinks = self.patches[source_name]
            sinks = []
            for s in patch_sinks:
                if str(type(s.handler)) == "<class 'app.Application.PassthroughModule'>": # i'm not proud of that hack
                    if self.patches.get(s.handler.source_name):
                        sinks.extend(self.patches[s.handler.source_name])
                        changed = changed+1
                else:
                    sinks.append(s)
                
            if sinks and len(sinks) == 1 and sinks[0].handler:
                del self.patches[source_name]
                source.handler = sinks[0].handler
                changed = changed + 1
        return changed > 0


    def createPatch(self, src, dst):
        if self.stringType == type(src):
            src = self.createPoint(src, SOURCE_POINT)
        if self.stringType == type(dst):
            dst = self.createPoint(dst, SINK_POINT)
        if src.inout != SOURCE_POINT:
            raise
        if dst.inout != SINK_POINT:
            raise
        if not src.name in self.patches:
            self.patches[src.name] = []
        self.patches[src.name].append(dst)


    def add(self, event, point):
        if not point:
            return
        if self.stringType == type(point):
            point = self.createPoint(point)
        self.dispatchEvent(event, point)
        # patchevent = PatchQueueEvent(event, point)
        # self.queue.add(patchevent)


    def add_first(self, event, point=None):
        if type(event) == type((1,2,3)):
            return
        if not point:
            return
        if self.stringType == type(point):
            point = self.createPoint(point)
        if 0==0:
            self.dispatchEvent(event, point)
            return
        patchevent = PatchQueueEvent(event, point)
        self.queue.add_first(patchevent)


    def delay(self, event, delay, point = None):
        if type(event) == type((1,2,3)):
            return
        if not point:
            return

        if self.stringType == type(point):
            point = self.createPoint(point)
        patchevent = PatchQueueEvent(event, point)
        self.queue.delay(patchevent, delay)

    
    def remove_all(self, fn, point = None):
        self.queue.remove_all(lambda pev : not point or point==pev.point and fn(pev.event))


    def process(self):
        patchEvent = self.queue.get()
        if not patchEvent:
            return False
        if not patchEvent.point:
            return True
        self.dispatchEvent(patchEvent.event, patchEvent.point)


    def dispatchEvent(self, event, point):
        _THREAD_LOCK_ and _THREAD_LOCK_.acquire()
        if point.handler:
            if point.handler.handle:
                point.handler.handle(event)
            else:
                point.handler(event)

        if point.name in self.patches:
            points = self.patches[point.name]
            for p in points:
                self.dispatchEvent(event, p)
        _THREAD_LOCK_ and _THREAD_LOCK_.release()



    def printSources(self):
        for name in self.points:
            point = self.points[name]
            if point.inout == SOURCE_POINT:
                print("    " + name)
        return

    def printSinks(self):
        for name in self.points:
            point = self.points[name]
            if point.inout == SINK_POINT:
                print("    " + name)
        return

    def printPatches(self):
        for src in self.patches:
            for dst in self.patches[src]:
                print("    " + src + " -> " + dst.name)
        return
