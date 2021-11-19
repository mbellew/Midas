EVENT_MAX = 100

def allocate_event():
    global EVENT_MAX
    ret = EVENT_MAX
    EVENT_MAX = EVENT_MAX + 1
    return ret

EVENT_DELETED = -1
EVENT_DONE = 0
EVENT_CONTINUE = 1

EVENT_PULSE=allocate_event()        # 24 per tempo
EVENT_TEMPO=allocate_event()        # e.g 130/minute
EVENT_MEASURE=allocate_event()      # usually 2, 3 or 4 tempo
EVENT_MIDI=allocate_event()
