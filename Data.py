

executionTime = 0
processQueue2 = []
processQueue3 = []

readyQueue = []
cpuQueue = []
finishedProcesses = []
waitingInIO = []

#                   fcfs  sjf  mlfq
cpuUtilization =      [0, 0, 0]
finalExecutionTimes = [0, 0, 0]

#             Tr   Tw   Ttr
#             [0]  [0]  [0]
avgTimes = [
    [0, 0, 0],  # fcfs
    [0, 0, 0],  # sjf
    [0, 0, 0],  # mlfq
]

#   Has Run  pID     Tr     Tw     Ttr
#     [0]     [0]    [0]    [0]     [0]
dataBank = [
    [0, 0, 0, 0, 0],  # p1
    [0, 0, 0, 0, 0],  # p2
    [0, 0, 0, 0, 0],  # p3
    [0, 0, 0, 0, 0],  # p4
    [0, 0, 0, 0, 0],  # p5
    [0, 0, 0, 0, 0],  # p6
    [0, 0, 0, 0, 0],  # p7
    [0, 0, 0, 0, 0]  # p8
]

dataBankFCFS = [
    [0, 0, 0, 0, 0],  # p1
    [0, 0, 0, 0, 0],  # p2
    [0, 0, 0, 0, 0],  # p3
    [0, 0, 0, 0, 0],  # p4
    [0, 0, 0, 0, 0],  # p5
    [0, 0, 0, 0, 0],  # p6
    [0, 0, 0, 0, 0],  # p7
    [0, 0, 0, 0, 0]  # p8
]

dataBankSJF = [
    [0, 0, 0, 0, 0],  # p1
    [0, 0, 0, 0, 0],  # p2
    [0, 0, 0, 0, 0],  # p3
    [0, 0, 0, 0, 0],  # p4
    [0, 0, 0, 0, 0],  # p5
    [0, 0, 0, 0, 0],  # p6
    [0, 0, 0, 0, 0],  # p7
    [0, 0, 0, 0, 0]  # p8
]

dataBankMLFQ = [
    [0, 0, 0, 0, 0],  # p1
    [0, 0, 0, 0, 0],  # p2
    [0, 0, 0, 0, 0],  # p3
    [0, 0, 0, 0, 0],  # p4
    [0, 0, 0, 0, 0],  # p5
    [0, 0, 0, 0, 0],  # p6
    [0, 0, 0, 0, 0],  # p7
    [0, 0, 0, 0, 0]  # p8
]

dataBanks = [dataBankFCFS, dataBankSJF, dataBankMLFQ]


def add(p):
    readyQueue.append(p)


def fromReadyToCPU():
    cpuQueue.append(readyQueue[0])
    readyQueue.pop(0)
    print(f"Ready Queue:", readyQueue)
    print(f"CPU Queue:", cpuQueue)


def fromCPUToIO():
    waitingInIO.append(cpuQueue[0])
    cpuQueue.pop(0)


