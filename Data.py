

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

def add(processs):
    readyQueue.append(processs)


def decIO(waitingInIO, processList,readyQueue):
    try:
        # for process in range(len(waitingInIO)):
        processs = 0
        while processs in range(len(waitingInIO)):
            p = processList[waitingInIO[processs] - 1]
            p.io_burst[0] -= 1
            # for i in range(len(p1.io_burst)):
            #    print(p1.io_burst[i])
            if p.io_burst[0] == 0:
                p.io_burst.pop(0)
                readyQueue.append(p.pID)
                waitingInIO.remove(p.pID)
                print(f'P{p.pID} has left the IO')
            # for c in waitingInIO:
            #    print(f'I/O Queue: Process', processList[c - 1].pID, "will be out of the IO in", processList[c - 1].io_burst[0])
            processs += 1

    except:  # debugging
        print(f'IO Queue: {waitingInIO}')
        print(p, 'broke in decIO')
        print(f'Ready Queue: {readyQueue}')
        for c in waitingInIO:
            print(f'I/O Queue: Process', processList[c - 1].pID, "will be out of the IO at",
                  processList[c - 1].ioWaitTime)
        exit()


def saveData(dataBankIndex, wastedTime=None):
    avgTat = 0
    avgTr = 0
    avgTwt = 0
    cpuUtilTemp = 0
    finishedProcesses.sort()
    finalExecutionTimes[dataBankIndex] = executionTime
    cpuUtilTemp = ((executionTime - wastedTime) / executionTime) * 100
    cpuUtilization[dataBankIndex] = round(cpuUtilTemp, 3)
    for i in range(8):
        for j in range(5):
            dataBanks[dataBankIndex][i][j] = dataBank[i][
                j]  # copies data from the data bank, which was gathered during the algorithm, into data bank specifically made for that algorithm
            dataBank[i][j] = 0
    for q in finishedProcesses:
        avgTat += dataBanks[dataBankIndex][q - 1][4]  # Turnaround Time
        avgTr += dataBanks[dataBankIndex][q - 1][2]  # Response Time
        avgTwt += dataBanks[dataBankIndex][q - 1][3]  # Waiting Time
    avgTimes[dataBankIndex][2] = avgTat / len(finishedProcesses)  # Turnaround Time
    avgTimes[dataBankIndex][0] = avgTr / len(finishedProcesses)  # Response Time
    avgTimes[dataBankIndex][1] = avgTwt / len(finishedProcesses)  # Waiting Time


def sortReadyQueue(readyQueue, processList):
    if len(readyQueue) > 1:
        n = len(readyQueue)
        for i in range(n):
            already_sorted = True
            for j in range(n - i - 1):
                if processList[readyQueue[j] - 1].cpu_burst[0] > processList[readyQueue[j + 1] - 1].cpu_burst[0]:
                    readyQueue[j], readyQueue[j + 1] = readyQueue[j + 1], readyQueue[j]
                    already_sorted = False
            if already_sorted:
                break
    else:
        pass




def saveData(dataBankIndex, wastedTime, executionTime, finishedProcesses):
    avgTat = 0
    avgTr = 0
    avgTwt = 0
    cpuUtilTemp = 0

    finishedProcesses.sort()

    finalExecutionTimes[dataBankIndex] = executionTime
    cpuUtilTemp = ((executionTime - wastedTime) / executionTime) * 100
    cpuUtilization[dataBankIndex] = round(cpuUtilTemp, 3)

    for q in finishedProcesses:

        avgTr += dataBanks[dataBankIndex][q - 1][2]  # Response Time
        avgTwt += dataBanks[dataBankIndex][q - 1][3]  # Waiting Time
        avgTat += dataBanks[dataBankIndex][q - 1][4]  # Turnaround Time


    avgTimes[dataBankIndex][0] = avgTr / len(finishedProcesses)  # Response Time
    avgTimes[dataBankIndex][1] = avgTwt / len(finishedProcesses)  # Waiting Time
    avgTimes[dataBankIndex][2] = avgTat / len(finishedProcesses)  # Turnaround Time

    print("Data Saved")