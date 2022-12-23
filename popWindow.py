import tkinter as tk
from Data import avgTimes, cpuUtilization, finalExecutionTimes


def dataInWindow():
    window = tk.Tk()
    window.title("Results")
    window.configure(bg="gray")
    window.geometry("450x300")

    label = tk.Label(window, text='Scheduler Results', font=("Times New Roman", 17), bg="gray")
    label.pack()

    labelgrid = tk.Frame(window, bg="gray")
    labelgrid.columnconfigure(0, weight=1)
    labelgrid.columnconfigure(1, weight=1)
    labelgrid.columnconfigure(2, weight=1)
    labelgrid.columnconfigure(3, weight=1)
    labelgrid.columnconfigure(4, weight=1)
    labelgrid.columnconfigure(5, weight=1)
    labelgrid.columnconfigure(6, weight=1)

    label1 = tk.Label(labelgrid, text='Scheduling Type', font=("Times New Roman", 17), bg="gray")
    label1.grid(row=0, column=0, sticky=tk.W)

    label5 = tk.Label(labelgrid, text='AVG Wait Time', font=("Times New Roman", 17), bg="gray")
    label5.grid(row=2, column=0, sticky=tk.W)

    label9 = tk.Label(labelgrid, text='AVG Turnaround', font=("Times New Roman", 17), bg="gray")
    label9.grid(row=3, column=0, sticky=tk.W)

    label13 = tk.Label(labelgrid, text='AVG Response', font=("Times New Roman", 17), bg="gray")
    label13.grid(row=1, column=0, sticky=tk.W)

    label17 = tk.Label(labelgrid, text='CPU Utilziation', font=("Times New Roman", 17), bg="gray")
    label17.grid(row=4, column=0, sticky=tk.W)

    label21 = tk.Label(labelgrid, text='Total Time', font=("Times New Roman", 17), bg="gray")
    label21.grid(row=5, column=0, sticky=tk.W)


    # First Come First Served Scheduler Data Labels
    label2 = tk.Label(labelgrid, text='FCFS', font=("Times New Roman", 17), bg="gray")
    label2.grid(row=0, column=2, sticky=tk.N)

    for i in range(3):
        labelFCFSTimes = tk.Label(labelgrid, text=f'{avgTimes[0][i]}', font=("Times New Roman", 17), bg="gray")
        labelFCFSTimes.grid(row=i + 1, column=2, sticky=tk.N)

    labelFCFSCPUUtil = tk.Label(labelgrid, text=f'{cpuUtilization[0]}%', font=("Times New Roman", 17), bg="gray")
    labelFCFSCPUUtil.grid(row=4, column=2, sticky=tk.N)
    labelFCFSTotalTime = tk.Label(labelgrid, text=f'{finalExecutionTimes[0]}', font=("Times New Roman", 17), bg="gray")
    labelFCFSTotalTime.grid(row=5, column=2, sticky=tk.N)


    # Shortest Job First Scheduler Data Labels
    label3 = tk.Label(labelgrid, text='SJF', font=("Times New Roman", 17), bg="gray")
    label3.grid(row=0, column=4, sticky=tk.N)

    for i in range(3):
        labelSJFTimes = tk.Label(labelgrid, text=f'{avgTimes[1][i]}', font=("Times New Roman", 17), bg="gray")
        labelSJFTimes.grid(row=i + 1, column=4, sticky=tk.N)

    labelSJFCPUUtil = tk.Label(labelgrid, text=f'{cpuUtilization[1]}%', font=("Times New Roman", 17), bg="gray")
    labelSJFCPUUtil.grid(row=4, column=4, sticky=tk.N)
    labelSJFTotalTime = tk.Label(labelgrid, text=f'{finalExecutionTimes[1]}', font=("Times New Roman", 17), bg="gray")
    labelSJFTotalTime.grid(row=5, column=4, sticky=tk.N)


    # Multilevel Feedback Queue Scheduler Data Labels
    label4 = tk.Label(labelgrid, text='MLFQ', font=("Times New Roman", 17), bg="gray")
    label4.grid(row=0, column=6, sticky=tk.N)
    for i in range(3):
        labelMLFQTimes = tk.Label(labelgrid, text=f'{avgTimes[2][i]}', font=("Times New Roman", 17), bg="gray")
        labelMLFQTimes.grid(row=i + 1, column=6, sticky=tk.N)

    labelMLFQCPUUtil = tk.Label(labelgrid, text=f'{cpuUtilization[2]}%', font=("Times New Roman", 17), bg="gray")
    labelMLFQCPUUtil.grid(row=4, column=6, sticky=tk.N)
    labelMLFQTotalTime = tk.Label(labelgrid, text=f'{finalExecutionTimes[2]}', font=("Times New Roman", 17), bg="gray")
    labelMLFQTotalTime.grid(row=5, column=6, sticky=tk.N)

    for i in range(6):
        labelSpacer1 = tk.Label(labelgrid, text='|', font=("Times New Roman", 17), bg="gray")
        labelSpacer1.grid(row=i, column=1, sticky=tk.W)
        labelSpacer2 = tk.Label(labelgrid, text='|', font=("Times New Roman", 17), bg="gray")
        labelSpacer2.grid(row=i, column=3, sticky=tk.W)
        labelSpacer3 = tk.Label(labelgrid, text='|', font=("Times New Roman", 17), bg="gray")
        labelSpacer3.grid(row=i, column=5, sticky=tk.W)

    labelgrid.pack()

    window.mainloop()
