from datetime import datetime


class TimeKeeper:
    def __init__(self, bpm):
        self.bpm = bpm
        self.start_time = -1
        self.ppq = 24
        pps = float(bpm)*self.ppq/60.0
        self.pulse_length = 1.0 / pps
        self.current_pulse = 0
        self.quarters_per_measure = 4
        self.pulses_per_measure = self.ppq * self.quarters_per_measure


    def reset(self):
        self.start_time = -1


    def get_time(self):
        return self.current_pulse


    def get_pulse_in_measure(self):
        return self.current_pulse % self.pulses_per_measure


    def update(self):
        time = datetime.now()
        if self.start_time == -1:
            self.start_time = time
        elapsed = (time - self.start_time)
        self.current_pulse = int(elapsed.total_seconds()/self.pulse_length)
        return self.current_pulse
