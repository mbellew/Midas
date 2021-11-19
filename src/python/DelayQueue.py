from heapq import * 


class DelayQueue:
    """
    EventQueue wraps a simple fifo queue and a priority queue for scheduling.  Events are removed from the scheduling
    queue based on the clock.get_time().  The queue is agnostic about the units of 'time' and what an 'event' looks like.
    """
    def __init__(self, clock):
        self.fifo = []
        self.scheduled = []
        self.event_counter = 0
        self.clock = clock
        self.deleted_event = "~~~THIS EVENT HAS BEEN DELETED~~~"
        return


    def add_first(self, event):
        self.fifo.insert(0, event)


    def add(self, event):
        self.fifo.append(event)
        return


    def schedule(self, event, time):
        """Schedule this event to be returned at time 'time'"""
        self.event_counter += 1
        heappush(self.scheduled, (time,self.event_counter,event))
        return


    def delay(self, event, delay):
        """Schedule this event to be returned after the delay 'current_time + delay'"""
        if delay <= 0:
            self.add(event)
        self.schedule(event, self.clock.get_time() + delay)
        return


    def remove(self, fn):
        for i in range(0,len(self.fifo)):
            if fn(self.fifo[i]):
                self.fifo.pop(i)
                return
        for i in range(0,len(self.scheduled)):
            if fn(self.scheduled[i]):
                self.fifo[i][0] = -1
                return


    def remove_all(self, fn):
        for i in range(len(self.fifo)-1,-1,-1):
            if fn(self.fifo[i]):
                self.fifo.pop(i)
        for i in range(0,len(self.scheduled)):
            entry = self.scheduled[i]
            if entry[2] != self.deleted_event and fn(entry[2]):
                self.scheduled[i] = (entry[0], entry[1], self.deleted_event)


    def get(self):
        while True:
            e = self._get()
            if not e == self.deleted_event:
                return e


    def _get(self):
        if 0 < len(self.fifo):
            return self.fifo.pop(0)
        time = self.clock.get_time()
        while 0 < len(self.scheduled) and self.scheduled[0][0] <= time:
            e = heappop(self.scheduled)[2]
            if not e == self.deleted_event:
                self.fifo.append(e)
        if 0 < len(self.fifo):
            return self.fifo.pop(0)
        return None