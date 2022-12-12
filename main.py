# -*- coding: utf-8 -*-

from Process import Process
from Data import *

executionTime = 0

p1 = Process(1, [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4])
p2 = Process(2, [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8], )
p3 = Process(3, [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6])
p4 = Process(4, [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3])
p5 = Process(5, [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4])
p6 = Process(6, [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8])
p7 = Process(7, [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10])
p8 = Process(8, [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6])
processList = [p1, p2, p3, p4, p5, p6, p7, p8]


def loadReadyQueue():
    for j in processList:
        j.parse()
    for processes in range(len(processList)):
        add(processList[processes].pID)


def FCFS():
    loadReadyQueue()
    resetDataBank()
    print(f'Ready Queue:{readyQueue}')
    global wastedTime
    wastedTime = 0
    global executionTime
    executionTime = 0

    while len(readyQueue) > 0:
        fromReadyToCPU()
        printOnContextSwitch()
        currentProcess = processList[cpuQueue[0] - 1]

        if dataBank[currentProcess.pID - 1][0] == 0:  # first time running marker
            dataBank[currentProcess.pID - 1][2] = executionTime  # saving the response time
            dataBank[currentProcess.pID - 1][0] = 1

        while currentProcess.cpu_burst[0] > 0:
            executionTime += 1
            currentProcess.cpu_burst[0] -= 1
            print(f'Execution Time:{executionTime} - P{currentProcess.pID} is Running')
            decIO()
            countWait()

        if currentProcess.cpu_burst[0] == 0:
            print("Process {} has run. Execution time: {}".format(currentProcess.pID, executionTime))
            currentProcess.cpu_burst.pop(0)

            try:
                # currentProcess.ioWaitTime = executionTime + currentProcess.io_burst[0]
                # currentProcess.io_burst.pop(0)
                if not currentProcess.io_burst:
                    finishedProcesses.append(currentProcess.pID)
                    cpuQueue.pop(0)
                    print(f'P{currentProcess.pID} had finished')
                    dataBank[currentProcess.pID - 1][4] = executionTime  # sets turnaround time
                else:
                    fromCPUToIO()

                print(f'IO Queue: {waitingInIO}')
                for c in waitingInIO:
                    print(f'I/O Queue: Process', processList[c - 1].pID, "will be out of the IO in",
                          processList[c - 1].io_burst[0])
            except IndexError:
                finishedProcesses.append(currentProcess.pID)
                cpuQueue.pop(0)

        while readyQueue == [] and waitingInIO:
            print(f'CPU IDLING\t Execution Time:{executionTime}')
            decIO()
            wastedTime += 1
            executionTime += 1
            print(f'Finished Processes: {finishedProcesses}')

        if not readyQueue and not waitingInIO and not cpuQueue:
            saveData(0, wastedTime)

            print('FCFS Complete')


def SJF():
    loadReadyQueue()
    finishedProcesses = []

    print(f'Ready Queue:{readyQueue}')
    global wastedTime
    wastedTime = 0
    global executionTime
    executionTime = 0
    while len(readyQueue) > 0:
        sortReadyQueue()
        fromReadyToCPU()
        printOnContextSwitch()
        currentProcess = processList[cpuQueue[0] - 1]
        if dataBank[currentProcess.pID - 1][0] == 0:  # first time running marker
            dataBank[currentProcess.pID - 1][2] = executionTime  # saving the response time
            dataBank[currentProcess.pID - 1][0] = 1
        while currentProcess.cpu_burst[0] > 0:
            executionTime += 1
            currentProcess.cpu_burst[0] -= 1
            print(f'Execution Time:{executionTime} - P{currentProcess.pID} is Running')
            decIO()
            countWait()
        if currentProcess.cpu_burst[0] == 0:
            print("Process {} has run. Execution time: {}".format(currentProcess.pID, executionTime))
            currentProcess.cpu_burst.pop(0)
            try:
                # currentProcess.ioWaitTime = executionTime + currentProcess.io_burst[0]
                # currentProcess.io_burst.pop(0)
                if not currentProcess.io_burst:
                    finishedProcesses.append(currentProcess.pID)
                    cpuQueue.pop(0)
                    print(f'P{currentProcess.pID} had finished')
                    dataBank[currentProcess.pID - 1][4] = executionTime  # sets turnaround time
                else:
                    fromCPUToIO()
                print(f'IO Queue: {waitingInIO}')
                for c in waitingInIO:
                    print(f'I/O Queue: Process', processList[c - 1].pID, "will be out of the IO in",
                          processList[c - 1].io_burst[0])
            except IndexError:
                finishedProcesses.append(currentProcess.pID)
                cpuQueue.pop(0)
        while readyQueue == [] and waitingInIO:
            print(f'CPU IDLING\t Execution Time:{executionTime}')
            decIO()
            wastedTime += 1
            executionTime += 1
            print(f'Finished Processes: {finishedProcesses}')
        if not readyQueue and not waitingInIO and not cpuQueue:
            saveData(1, wastedTime)  # data bank index key: FCFS = 0; SJF = 1; MLFQ = 2
            print('SJF Complete')


def MLFQ():
    finishedProcesses = []
    wastedTime = 0
    executionTime = 0
    timeQuantum = 0
    loadReadyQueue()
    finishedProcesses = []

    print("MLFQ Start")
    while readyQueue or processQueue2 or processQueue3 or waitingInIO:
        while len(readyQueue) > 0:  # RR for Priority Queue 1
            printOnContextSwitch()
            fromReadyToCPU()

            currentProcess = processList[cpuQueue[0] - 1]

            if dataBank[currentProcess.pID - 1][0] == 0:  # first time running marker
                dataBank[currentProcess.pID - 1][2] = executionTime  # saving the response time
                dataBank[currentProcess.pID - 1][0] = 1
            timeQuantum = 0
            while currentProcess.cpu_burst[0] > 0 and timeQuantum < 5:
                executionTime += 1
                currentProcess.cpu_burst[0] -= 1
                timeQuantum += 1
                print(f'Execution Time:{executionTime} - P{currentProcess.pID} is Running - Tq: {timeQuantum}')
                decIO()
                countWait()
                if timeQuantum == 5 and currentProcess.cpu_burst[0] > 0:
                    demoteProcessToP2(currentProcess)
                    timeQuantum = 0
                    break

                if currentProcess.cpu_burst[0] == 0:
                    print("Process {} has run. Execution time: {}".format(currentProcess.pID, executionTime))
                    currentProcess.cpu_burst.pop(0)

                    try:

                        if not currentProcess.io_burst:
                            finishedProcesses.append(currentProcess.pID)
                            cpuQueue.pop(0)
                            print(f'P{currentProcess.pID} had finished')
                            dataBank[currentProcess.pID - 1][4] = executionTime  # sets turnaround time
                            break
                        else:
                            fromCPUToIO()
                            break

                        print(f'IO Queue: {waitingInIO}')
                        for c in waitingInIO:
                            print(f'I/O Queue: Process', processList[c - 1].pID, "will be out of the IO in",
                                  processList[c - 1].io_burst[0])
                        break
                    except IndexError:  # if no more cpu bursts
                        finishedProcesses.append(currentProcess.pID)
                        cpuQueue.pop(0)

        while readyQueue == [] and len(processQueue2) > 0:  # RR for Priority Queue 2

            print('///////////////////////////////////////////////////////////\n'
                  '//////////////    Context Switch    ///////////////////////\n'
                  '///////////////////////////////////////////////////////////')

            processQueue2WithTimes = []

            for i in processQueue2:
                processQueue2WithTimes.append(f'P{i}:{processList[i - 1].cpu_burst[0]}')
            print(f'Ready Queue 2: {processQueue2WithTimes}')

            cpuQueue.append(processQueue2[0])
            processQueue2.pop(0)

            currentProcess = processList[cpuQueue[0] - 1]

            timeQuantum = 0
            while currentProcess.cpu_burst[0] > 0 and timeQuantum < 10:
                executionTime += 1
                currentProcess.cpu_burst[0] -= 1
                timeQuantum += 1
                print(f'Execution Time:{executionTime} - P{currentProcess.pID} is Running - Tq: {timeQuantum}')
                decIO()
                countWait()

                if timeQuantum == 10 and currentProcess.cpu_burst[0] > 0:
                    demoteProcessToP3(currentProcess)
                    timeQuantum = 0
                    break

                if currentProcess.cpu_burst[0] == 0:
                    print("Process {} has run. Execution time: {}".format(currentProcess.pID, executionTime))
                    currentProcess.cpu_burst.pop(0)
                    print(currentProcess.cpu_burst)
                    print(f'Process Queue 3 :{processQueue3}')

                    try:

                        if not currentProcess.io_burst:
                            finishedProcesses.append(currentProcess.pID)
                            cpuQueue.pop(0)
                            print(f'P{currentProcess.pID} had finished')
                            dataBank[currentProcess.pID - 1][4] = executionTime  # sets turnaround time
                            break
                        else:
                            fromCPUToIO()
                            break

                        print(f'IO Queue: {waitingInIO}')
                        for c in waitingInIO:
                            print(f'I/O Queue: Process', processList[c - 1].pID, "will be out of the IO in",
                                  processList[c - 1].io_burst[0])
                        break
                    except IndexError:
                        finishedProcesses.append(currentProcess.pID)
                        cpuQueue.pop(0)
                        break

        while readyQueue == [] and processQueue2 == [] and len(processQueue3) > 0:

            print('/////////////////////////////////////////////////\n'
                  '//////////////    Context Switch   //////////////\n'
                  '/////////////////////////////////////////////////')
            processQueue3WithTimes = []
            print(f'Execution Time: {executionTime}')

            for i in processQueue3:
                processQueue3WithTimes.append(f'P{i}:{processList[i - 1].cpu_burst[0]}')
            print(f'Ready Queue 3: {processQueue3WithTimes}')

            cpuQueue.append(processQueue3[0])
            processQueue3.pop(0)

            currentProcess = processList[cpuQueue[0] - 1]
            while currentProcess.cpu_burst[0] > 0:
                executionTime += 1
                currentProcess.cpu_burst[0] -= 1
                print(f'Execution Time:{executionTime} - P{currentProcess.pID} is Running')
                decIO()
                countWait()

            if currentProcess.cpu_burst[0] == 0:
                print("Process {} has run. Execution time: {}".format(currentProcess.pID, executionTime))
                currentProcess.cpu_burst.pop(0)

                try:

                    if not currentProcess.io_burst:
                        finishedProcesses.append(currentProcess.pID)
                        cpuQueue.pop(0)
                        print(f'P{currentProcess.pID} had finished')
                        dataBank[currentProcess.pID - 1][4] = executionTime  # sets turnaround time
                    else:
                        fromCPUToIO()

                    print(f'IO Queue: {waitingInIO}')
                    for c in waitingInIO:
                        print(f'I/O Queue: Process', processList[c - 1].pID, "will be out of the IO in",
                              processList[c - 1].io_burst[0])
                except IndexError:
                    finishedProcesses.append(currentProcess.pID)
                    cpuQueue.pop(0)

        while processQueue3 == [] and waitingInIO and not processQueue2 and not readyQueue:
            print(f'CPU IDLING\t Execution Time:{executionTime}')
            decIO()
            wastedTime += 1
            executionTime += 1
            print(f'Finished Processes: {finishedProcesses}')

            for i in waitingInIO:
                print(f'I/O Queue: Process', processList[i - 1].pID, "will be out of the IO in",
                      processList[i - 1].io_burst[0])
        if not readyQueue and not waitingInIO and not cpuQueue and not processQueue2 and not processQueue3:
            saveData(2, wastedTime)  # data bank index key: FCFS = 0; SJF = 1; MLFQ = 2
            print('MLFQ Complete')


def demoteProcessToP2(process):
    cpuQueue.pop(0)
    processQueue2.append(process.pID)
    print(processQueue2)


def demoteProcessToP3(process):
    cpuQueue.pop(0)
    processQueue3.append(process.pID)


def countWait():
    for process in readyQueue:  # processes start use process ID so -1 to properly index
        dataBank[process - 1][3] += 1
    for process in processQueue2:  # processes start use process ID so -1 to properly index
        dataBank[process - 1][3] += 1
    for process in processQueue3:  # processes start use process ID so -1 to properly index
        dataBank[process - 1][3] += 1


def countWait():
    for process in readyQueue:  # processes start use process ID so -1 to properly index
        dataBank[process - 1][3] += 1
    for process in processQueue2:  # processes start use process ID so -1 to properly index
        dataBank[process - 1][3] += 1
    for process in processQueue3:  # processes start use process ID so -1 to properly index
        dataBank[process - 1][3] += 1


def decIO():
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
                print('P{} has left the IO'.format(p.pID))
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




def sortReadyQueue():
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


def decIO():
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
                print('P{} has left the IO'.format(p.pID))
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


def saveData(dataBankIndex, wastedTime):
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


def printData():
    # finishedProcesses.sort()

    print(
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ╔═══════════════════════════════════════════════════════╗\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ║                    Final Analytics                    ║\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ╚═══════════════════════════════════════════════════════╝\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   \n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ╔═════════════════╦═══════════╦════════════╦════════════╗\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ║ Scheduling Type ║    SJF    ║    FCFS    ║    MLFQ    ║\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ╠═════════════════╬═══════════╬════════════╬════════════╣\n'
        f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ║  AVG Wait Time  ║   {avgTimes[1][1]}  ║    {avgTimes[0][1]}   ║   {avgTimes[2][1]}  ║\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ╠═════════════════╬═══════════╬════════════╬════════════╣\n'
        f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ║  AVG Turnaround ║  {avgTimes[1][2]}  ║   {avgTimes[0][2]}   ║   {avgTimes[2][2]}  ║\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ╠═════════════════╬═══════════╬════════════╬════════════╣\n'
        f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ║  AVG Response   ║  {avgTimes[1][0]}   ║   {avgTimes[0][0]}   ║   {avgTimes[2][0]}    ║\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ╠═════════════════╬═══════════╬════════════╬════════════╣\n'
        f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ║ CPU Utilization ║  {cpuUtilization[1]}%  ║   {cpuUtilization[0]}%  ║   {cpuUtilization[2]}%   ║\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ╠═════════════════╬═══════════╬════════════╬════════════╣\n'
        f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ║   Total  Time   ║     {finalExecutionTimes[1]}   ║     {finalExecutionTimes[0]}    ║     {finalExecutionTimes[2]}    ║\n'
        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ╚═════════════════╩═══════════╩════════════╩════════════╝\n\n\n'










        '╔═══════════════════════════════════════════════════════════╗\t\t ╔═══════════════════════════════════════════════════════════╗\t\t ╔═══════════════════════════════════════════════════════════╗\n'
        '║                  First Come  First Serve                  ║\t\t ║                    Shortest Job First                     ║\t\t ║                 Multilevel Feedback Queue                 ║\n'
        '╠═══════════════════════════════════════════════════════════╣\t\t ╠═══════════════════════════════════════════════════════════╣\t\t ╠═══════════════════════════════════════════════════════════╣\n'
        '   Process     Waiting Time  Turnaround Time  Response Time  \t\t    Process     Waiting Time  Turnaround Time  Response Time   \t\t    Process     Waiting Time  Turnaround Time  Response Time  '
    )
    for i in range(8):
        print(
            f' \t  P{i + 1}             {dataBankFCFS[i][3]}               {dataBankFCFS[i][4]} \t\t\t    {dataBankFCFS[i][2]}    \t\t '
            f' \t  P{i + 1}             {dataBankSJF[i][3]}               {dataBankSJF[i][4]} \t\t\t     {dataBankSJF[i][2]}   \t\t '
            f' \t  P{i + 1}             {dataBankMLFQ[i][3]}               {dataBankMLFQ[i][4]} \t\t\t     {dataBankMLFQ[i][2]}   ')

    print(
        '═════════════════════════════════════════════════════════════\t\t ═════════════════════════════════════════════════════════════\t\t ═════════════════════════════════════════════════════════════\n')


def sortReadyQueue():
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


def printOnContextSwitch():
    print('///////////////////////////////////////////////////////////\n'
          '//////////////    Context Switch    ///////////////////////\n'
          '///////////////////////////////////////////////////////////')
    readyQueueWithTimes = []

    for i in readyQueue:
        readyQueueWithTimes.append(f'P{i}:{processList[i - 1].cpu_burst[0]}')
    print(f'Ready Queue: {readyQueueWithTimes}')


def resetDataBank():
    for i in range(8):
        for j in range(5):
            dataBank[i][j] = 0

def prepProcesslist():
    loadReadyQueue()
    finishedProcesses = []
    resetDataBank()


def printProcesslist():
    for i in (processList):
        print(f"Process {i.pID}: \nCPU Bursts: {i.cpu_burst} \nI/O Bursts: {i.io_burst}")
if __name__ == "__main__":
    printProcesslist()
    FCFS()
    printProcesslist()
    SJF()
    printProcesslist()
    MLFQ()

    printData()
