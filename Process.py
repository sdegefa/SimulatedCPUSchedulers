class Process:

    def __init__(self, pID, burst):
        self.pID = pID
        self.burst = burst

        self.cpu_burst = []
        self.io_burst = []
        self.ioWaitTime = 0

    def parse(self):
        for i in range(len(self.burst)):
            if i % 2 == 0:
                self.cpu_burst.append(self.burst[i])
            else:
                self.io_burst.append(self.burst[i])

    def getCPUBurst(self):
        return self.cpu_burst[0]

    def __repr__(self):
        return "Process('p{}', 'CPU Burst:{}', 'IO Burst:{}')".format(self.pID, self.cpu_burst, self.io_burst)




