from Data import dataBankSJF, avgTimes, decIO, sortReadyQueue, saveData


class sjf:

    def __init__(self, processList):
        self.pList = processList

    def run(self):
        print(self.pList)
        wastedTime = 0
        executionTime = 0
        waitingList = []
        readyQueue = []
        cpuQueue = []
        finishedProcesses = []

        for processes in range(len(self.pList)):  # loops through the process list and adds all to the ready queue to begin the scheduling algorithm
            readyQueue.append(self.pList[processes].pID)

        while len(readyQueue) > 0:
            sortReadyQueue(readyQueue, self.pList)

            # Moving Process from Ready Queue to CPU
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
            if dataBankSJF[currentProcess.pID - 1][0] == 0:  # first time running marker
                dataBankSJF[currentProcess.pID - 1][2] = executionTime  # saving the response time
                dataBankSJF[currentProcess.pID - 1][0] = 1
            while currentProcess.cpu_burst[0] > 0:
                executionTime += 1
                currentProcess.cpu_burst[0] -= 1
                print(f'Execution Time:{executionTime} - P{currentProcess.pID} is Running')
                decIO(waitingList, self.pList, readyQueue)
                # Counting Wait Times
                for process in readyQueue:  # processes start use process ID so -1 to properly index
                    dataBankSJF[process - 1][3] += 1

            if currentProcess.cpu_burst[0] == 0:
                print(f"Process {currentProcess.pID} has run. Execution time: {executionTime}")
                currentProcess.cpu_burst.pop(0)
                try:
                    # currentProcess.ioWaitTime = executionTime + currentProcess.io_burst[0]
                    # currentProcess.io_burst.pop(0)
                    if not currentProcess.io_burst:
                        finishedProcesses.append(currentProcess.pID)
                        cpuQueue.pop(0)
                        print(f'P{currentProcess.pID} had finished')
                        dataBankSJF[currentProcess.pID - 1][4] = executionTime  # sets turnaround time
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
            while readyQueue == [] and waitingList:
                print(f'CPU IDLING\t Execution Time:{executionTime}')
                decIO(waitingList, self.pList, readyQueue)
                wastedTime += 1
                executionTime += 1
                print(f'Finished Processes: {finishedProcesses}')
            if not readyQueue and not waitingList and not cpuQueue:
                saveData(1, wastedTime, executionTime, finishedProcesses)  # data bank index key: FCFS = 0; SJF = 1; MLFQ = 2

                print('SJF Complete')



