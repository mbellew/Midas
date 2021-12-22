EVENT_MAX = 100

def allocate_event():
    global EVENT_MAX
    ret = EVENT_MAX
    EVENT_MAX = EVENT_MAX + 1
    return ret

EVENT_DELETED = -1
EVENT_DONE = 0
EVENT_CONTINUE = 1


EVENT_CLOCK=allocate_event()        # ppq
EVENT_MIDI=allocate_event()
EVENT_KEYCHANGE=allocate_event()


# TODO use Event class instead of tuples

class Event:
    def __init__(self, code, source, obj):
        self.code = code
        self.source = source
        self.obj = obj

    def __str__(self):
        return str(self.code) + " - " + self.source + " " + str(self.obj)
