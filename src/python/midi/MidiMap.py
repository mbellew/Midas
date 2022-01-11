class MidiMap:
    def __init__(self):
        self.map = []

    def add(self, cc, lamb):
        while len(self.map) <= cc:
            self.map.append(None)
        self.map[cc] = lamb
    
    def dispatch(self, msg):
        if msg.control < len(self.map) and self.map[msg.control]:
            self.map[msg.control](msg)
