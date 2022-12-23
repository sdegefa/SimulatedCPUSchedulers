from Data import dataBankMLFQ, avgTimes, decIO, saveData


class mlfq:

    def __init__(self, processList):
        self.pList = processList

    def run(self):
        print(self.pList)
        wastedTime = 0
        executionTime = 0
        waitingList = []
        readyQueue = []
        processQueue2 = []
        processQueue3 = []
        cpuQueue = []
        finishedProcesses = []

        for processes in range(len(self.pList)):  # loops through the process list and adds all to the ready queue to begin the scheduling algorithm
            readyQueue.append(self.pList[processes].pID)

        while readyQueue or processQueue2 or processQueue3 or waitingList:
            while len(readyQueue) > 0:  # RR for Priority Queue 1
                # fromReadyToCPU()
                cpuQueue.append(readyQueue[0])
                readyQueue.pop(0)
                # Context Switch Data
                print('///////////////////////////////////////////////////////////\n'
                      '//////////////    Context Switch    ///////////////////////\n'
                      '///////////////////////////////////////////////////////////')
                readyQueueWithTimes = []

                for i in readyQueue:
                    readyQueueWithTimes.append(f'P{i}:{self.pList[i - 1].cpu_burst[0]}')
                print(f'Ready Queue: {readyQueueWithTimes}')

                currentProcess = self.pList[cpuQueue[0] - 1]

                if dataBankMLFQ[currentProcess.pID - 1][0] == 0:  # first time running marker
                    dataBankMLFQ[currentProcess.pID - 1][2] = executionTime  # saving the response time
                    dataBankMLFQ[currentProcess.pID - 1][0] = 1
                timeQuantum = 0
                while currentProcess.cpu_burst[0] > 0 and timeQuantum < 5:
                    executionTime += 1
                    currentProcess.cpu_burst[0] -= 1
                    timeQuantum += 1
                    print(f'Execution Time:{executionTime} - P{currentProcess.pID} is Running - Tq: {timeQuantum}')
                    decIO(waitingList, self.pList, readyQueue)
                    # Counting Wait Times
                    for process in readyQueue:
                        dataBankMLFQ[process - 1][3] += 1
                    for process in processQueue2:
                        dataBankMLFQ[process - 1][3] += 1
                    for process in processQueue3:
                        dataBankMLFQ[process - 1][3] += 1

                    if timeQuantum == 5 and currentProcess.cpu_burst[0] > 0:
                        # Demoting the Current Process To Process Queue 2
                        cpuQueue.pop(0)
                        processQueue2.append(currentProcess.pID)
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
                                dataBankMLFQ[currentProcess.pID - 1][4] = executionTime  # sets turnaround time
                                break
                            else:
                                # Moving Process from the CPU to I/O
                                waitingList.append(cpuQueue[0])
                                cpuQueue.pop(0)
                                break

                            print(f'IO Queue: {waitingList}')
                            for c in waitingList:
                                print(f'I/O Queue: Process', self.pList[c - 1].pID, "will be out of the IO in",
                                      self.pList[c - 1].io_burst[0])
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
                    processQueue2WithTimes.append(f'P{i}:{self.pList[i - 1].cpu_burst[0]}')
                print(f'Ready Queue 2: {processQueue2WithTimes}')

                cpuQueue.append(processQueue2[0])
                processQueue2.pop(0)

                currentProcess = self.pList[cpuQueue[0] - 1]

                timeQuantum = 0
                while currentProcess.cpu_burst[0] > 0 and timeQuantum < 10:
                    executionTime += 1
                    currentProcess.cpu_burst[0] -= 1
                    timeQuantum += 1
                    print(f'Execution Time:{executionTime} - P{currentProcess.pID} is Running - Tq: {timeQuantum}')
                    decIO(waitingList, self.pList, readyQueue)
                    # Counting Wait Times
                    for process in readyQueue:
                        dataBankMLFQ[process - 1][3] += 1
                    for process in processQueue2:
                        dataBankMLFQ[process - 1][3] += 1
                    for process in processQueue3:
                        dataBankMLFQ[process - 1][3] += 1

                    if timeQuantum == 10 and currentProcess.cpu_burst[0] > 0:
                        # Demoting Process To Process Queue 3
                        cpuQueue.pop(0)
                        processQueue3.append(currentProcess.pID)
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
                                dataBankMLFQ[currentProcess.pID - 1][4] = executionTime  # sets turnaround time
                                break
                            else:
                                # Moving Process from the CPU to I/O
                                waitingList.append(cpuQueue[0])
                                cpuQueue.pop(0)
                                break

                            print(f'IO Queue: {waitingList}')
                            for c in waitingList:
                                print(f'I/O Queue: Process', self.pList[c - 1].pID, "will be out of the IO in",
                                      self.pList[c - 1].io_burst[0])
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
                    processQueue3WithTimes.append(f'P{i}:{self.pList[i - 1].cpu_burst[0]}')
                print(f'Ready Queue 3: {processQueue3WithTimes}')

                cpuQueue.append(processQueue3[0])
                processQueue3.pop(0)

                currentProcess = self.pList[cpuQueue[0] - 1]
                while currentProcess.cpu_burst[0] > 0:
                    executionTime += 1
                    currentProcess.cpu_burst[0] -= 1
                    print(f'Execution Time:{executionTime} - P{currentProcess.pID} is Running')
                    decIO(waitingList, self.pList, readyQueue)
                    # Counting Wait Times
                    for process in readyQueue:
                        dataBankMLFQ[process - 1][3] += 1
                    for process in processQueue2:
                        dataBankMLFQ[process - 1][3] += 1
                    for process in processQueue3:
                        dataBankMLFQ[process - 1][3] += 1

                if currentProcess.cpu_burst[0] == 0:
                    print("Process {} has run. Execution time: {}".format(currentProcess.pID, executionTime))
                    currentProcess.cpu_burst.pop(0)

                    try:

                        if not currentProcess.io_burst:
                            finishedProcesses.append(currentProcess.pID)
                            cpuQueue.pop(0)
                            print(f'P{currentProcess.pID} had finished')
                            dataBankMLFQ[currentProcess.pID - 1][4] = executionTime  # sets turnaround time
                        else:
                            # Moving Process from the CPU to I/O
                            waitingList.append(cpuQueue[0])
                            cpuQueue.pop(0)

                        print(f'IO Queue: {waitingList}')
                        for c in waitingList:
                            print(f'I/O Queue: Process', self.pList[c - 1].pID, "will be out of the IO in",
                                  self.pList[c - 1].io_burst[0])
                    except IndexError:
                        finishedProcesses.append(currentProcess.pID)
                        cpuQueue.pop(0)

            while processQueue3 == [] and waitingList and not processQueue2 and not readyQueue:
                print(f'CPU IDLING\t Execution Time:{executionTime}')
                decIO(waitingList, self.pList, readyQueue)
                wastedTime += 1
                executionTime += 1
                print(f'Finished Processes: {finishedProcesses}')

                for i in waitingList:
                    print(f'I/O Queue: Process', self.pList[i - 1].pID, "will be out of the IO in",
                          self.pList[i - 1].io_burst[0])
            if not readyQueue and not waitingList and not cpuQueue and not processQueue2 and not processQueue3:
                saveData(2, wastedTime, executionTime, finishedProcesses)  # data bank index key: FCFS = 0; SJF = 1; MLFQ = 2

                print('MLFQ Complete')





