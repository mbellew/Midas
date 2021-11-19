from DelayQueue import DelayQueue


SINK_POINT = 100
SOURCE_POINT = 201


class Point:
    def __init__(self, queue, name, inout, handler):
        self.parent = queue
        self.name = name
        self.inout = inout
        self.handler = handler

    def add(self, event):
        self.parent.add(event, self)

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
    def __init__(self, clock):
        self.queue = DelayQueue(clock)
        self.points = {}
        self.patches = {}
        self.stringType = type('')
        self.listType = type((0,1))


    def createSink(self, sink, handler):
        return self.createPoint(sink, SINK_POINT, handler)


    def createSource(self, sourceName):
        return self.createPoint(sourceName, SOURCE_POINT)


    def createPoint(self, sink, inout, handler=None):
        if type(sink)==self.stringType:
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
        """Doesn't do anyting yet, but could"""
        pass


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


    def add(self, event, point = None):
        if self.stringType == type(point):
            point = self.createPoint(point)
        patchevent = PatchQueueEvent(event, point)
        self.queue.add(patchevent)


    def add_first(self, event, point = None):
        if self.stringType == type(point):
            point = self.createPoint(point)
        patchevent = PatchQueueEvent(event, point)
        self.queue.add_first(patchevent)


    def delay(self, event, delay, point = None):
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
            points = self.points.values()
        else:
            point = patchEvent.point
            points = None
            if point.inout == SINK_POINT:
                points = [point]
            elif point.name in self.patches:
                points = self.patches[point.name]

        if not points:
            return True
        for target in points:
            if target.handler:
                target.handler.handle(patchEvent.event)
