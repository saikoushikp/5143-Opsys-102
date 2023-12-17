import sys

import RichTable
 

class Queue:
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ",".join([str(pcb.pid) for pcb in self.queue])

    def addPCB(self, pcb):
        self.queue.append(pcb)

    def removePCB(self):
        item = self.queue[0]
        del self.queue[0]
        return item
    
    def decrement(self):
        """ Iterate over the self.queue and decrement or call whatever
            method for each of the pcb's in this queue
        """
        # for each process in queue
        #    call decrementIoBurst
        pass

    def incrememnt(self, what='waittime'):
        """ Iterate over the self.queue and decrement or call whatever
            method for each of the pcb's in this queue
        """
        if what == 'waittime':
            for pcb in self.queue:
                pcb.incrementWaitQueueTotalTime()
        elif what == 'runtime':
            for pcb in self.queue:
                pcb.incrementReadyQueueTotalTime()

class SysClock:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state
        if not 'clock' in self.__dict__: 
            self.clock = 0

    def increment(self):
        self.clock += 1

    def getClock(self):
        return self.clock
    
class CPU:
    def __init__(self):
        self.busy = False
        self.runningPCB = None
        self.totalExecutionTime = 0

    def incrementExecutionTime(self):
        self.totalExecutionTime += 1

    def decrementCurrentProcess(self):
        self.runningPCB.decrementCpuBurst()

    def loadProcess(self, pcb):
        self.runningPCB = pcb
        self.busy = True

    def KickOff(self):
        if self.runningPCB.getCurrentBurstTime() == 0:
            pcb = self.runningPCB
            self.busy = False
            self.runningPCB = None
            return pcb
        
    def removeProcess(self):
        self.runningPCB = None
        self.busy = False

class PCB:
    def __init__(self, pid, bursts, at, priority):
        self.pid = pid
        self.priority = priority
        self.arrivalTime = at
        self.bursts = bursts
        self.currBurstIndex = 0
        self.TAT = 0
        self.readyQueueTotalTime = 0
        self.waitQueueTotalTime = 0

    def decrementCpuBurst(self):
        self.bursts[self.currBurstIndex] -= 1

    def decrementIoBurst(self):
        self.bursts[self.currBurstIndex] -= 1

    def incrementBurstIndex(self):
        self.currBurstIndex += 1

    def getCurrentBurstTime(self):
        return self.bursts[self.currBurstIndex]

    def incrementReadyQueueTotalTime(self):
        self.readyQueueTotalTime += 1

    def incrementWaitQueueTotalTime(self):
        self.waitQueueTotalTime += 1

    def getArrivalTime(self):
        return self.arrivalTime
    
    def setTAT(self, t):
        self.TAT = t
    
class Simulator:
    def __init__(self, datfile, cpuCount=1, IOCount=1, timeSlice=None):
        self.datfile = datfile
        self.new = Queue()
        self.wait = Queue()
        self.ready = Queue()
        self.terminated = Queue()
        self.running = [CPU() for _ in range(cpuCount)]
        self.IOs = [CPU() for _ in range(IOCount)]
        self.systemClock = SysClock()
        self.timeSlice = int(timeSlice) if timeSlice else None
        
        self.richTable = RichTable.RichTable()

    def readData(self):
        with open(self.datfile) as f:
            self.data = f.read().split("\n")

        for process in self.data:
            if len(process) > 0:
                parts = process.split(' ')
                arrival = parts[0]
                pid = parts[1]
                priority = parts[2]
                bursts = parts[3:]
                if int(arrival) == self.systemClock.getClock():
                    for i in range(len(bursts)):
                        bursts[i] = int(bursts[i])
                    self.new.addPCB(PCB(int(pid), bursts, int(arrival), priority))
                    self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{pid} entered to New queue")
                    self.richTable.show_tables(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)


    def moveToReady(self):
        i = 0
        while i < len(self.new.queue):
            self.ready.addPCB(self.new.queue.pop(i))
            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{self.ready.queue[-1].pid} entered to Ready queue")

    def haveProcesses(self):
        haveProcesses = False
        if len(self.new.queue) > 0:
            haveProcesses = True
        if len(self.wait.queue) > 0:
            haveProcesses = True
        if len(self.ready.queue) > 0:
            haveProcesses = True

        for cpu in self.running:
            if cpu.busy:
                haveProcesses = True
                break
        for io in self.IOs:
            if io.busy:
                haveProcesses = True
                break
        return haveProcesses

    def FCFS(self):
        while self.haveProcesses():
            self.moveToReady()

            self.richTable.show_tables(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)

            for cpu in self.running:
                if cpu.busy:
                    cpu.incrementExecutionTime()
                    cpu.decrementCurrentProcess()
                    kickedOffProcess = cpu.KickOff()

                    if kickedOffProcess:
                        kickedOffProcess.incrementBurstIndex()
                        if kickedOffProcess.currBurstIndex == len(kickedOffProcess.bursts):
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.setTAT(self.systemClock.getClock() - kickedOffProcess.getArrivalTime())
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} terminated:\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT} \nRWT = {kickedOffProcess.readyQueueTotalTime}\nIWT = {kickedOffProcess.waitQueueTotalTime }")
                        else:
                            self.wait.addPCB(kickedOffProcess)
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} moved to Waiting queue")

            for io in self.IOs:
                if io.busy:
                    io.incrementExecutionTime()
                    io.decrementCurrentProcess()
                    kickedOffProcess = io.KickOff()
                    if kickedOffProcess:
                        kickedOffProcess.incrementBurstIndex()
                        if kickedOffProcess.currBurstIndex == len(kickedOffProcess.bursts):
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.setTAT(self.systemClock.getClock() - kickedOffProcess.getArrivalTime())
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} terminated:\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT} \nRWT = {kickedOffProcess.readyQueueTotalTime}\nIWT = {kickedOffProcess.waitQueueTotalTime }")
                        else:
                            self.ready.addPCB(kickedOffProcess)
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} moved to Ready queue")
                            
            if len(self.ready.queue) > 0: 
                for cpu in self.running:
                    if not cpu.busy:
                        cpu.loadProcess(self.ready.removePCB())
                        self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                        self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{cpu.runningPCB.pid} obtained CPU:{self.running.index(cpu)}")
                        if len(self.ready.queue) <= 0:
                            break

            if len(self.wait.queue) > 0:
                for io in self.IOs:
                    if not io.busy:
                        io.loadProcess(self.wait.removePCB())
                        self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                        self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{io.runningPCB.pid} obtained device:{self.IOs.index(io)}")
                        if len(self.wait.queue) <= 0:
                            break
            
            self.systemClock.increment()
            self.ready.incrememnt(what='runtime')
            self.wait.incrememnt(what='waittime')
            self.readData()

    def RR(self):
        """ Round Robin
        """
        while self.haveProcesses():
            self.moveToReady()
            
            self.richTable.show_tables(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)

            for cpu in self.running:
                if cpu.busy:
                    cpu.incrementExecutionTime()
                    cpu.decrementCurrentProcess()

                    kickedOffProcess = cpu.KickOff()
                    if not kickedOffProcess:
                        if cpu.totalExecutionTime % self.timeSlice == 0:
                            self.ready.addPCB(cpu.runningPCB)
                            cpu.removeProcess()
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{self.ready.queue[-1].pid} preempted")
                    else:
                        kickedOffProcess.incrementBurstIndex()
                        if kickedOffProcess.currBurstIndex == len(kickedOffProcess.bursts):
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.setTAT(self.systemClock.getClock() - kickedOffProcess.getArrivalTime())
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} terminated:\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT} \nRWT = {kickedOffProcess.readyQueueTotalTime}\nIWT = {kickedOffProcess.waitQueueTotalTime }")
                        else:
                            self.wait.addPCB(kickedOffProcess)
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} moved to Waiting queue")
            
            for io in self.IOs:
                if io.busy:
                    io.incrementExecutionTime()
                    io.decrementCurrentProcess()
                    kickedOffProcess = io.KickOff()
                    if kickedOffProcess:
                        kickedOffProcess.incrementBurstIndex()
                        if kickedOffProcess.currBurstIndex == len(kickedOffProcess.bursts):
                            self.terminated.addPCB(kickedOffProcess)                            
                            kickedOffProcess.setTAT(self.systemClock.getClock() - kickedOffProcess.getArrivalTime())
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} terminated:\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT} \nRWT = {kickedOffProcess.readyQueueTotalTime}\nIWT = {kickedOffProcess.waitQueueTotalTime }")
                        else:
                            self.ready.addPCB(kickedOffProcess)
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} moved to Ready queue")
            
            if len(self.ready.queue) > 0: 
                for cpu in self.running:
                    if not cpu.busy:
                        cpu.loadProcess(self.ready.removePCB())
                        self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                        self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{cpu.runningPCB.pid} obtained CPU:{self.running.index(cpu)}")
                        if len(self.ready.queue) <= 0:
                            break

            if len(self.wait.queue) > 0:
                for io in self.IOs:
                    if not io.busy:
                        io.loadProcess(self.wait.removePCB())
                        self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                        self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{io.runningPCB.pid} obtained device:{self.IOs.index(io)}")
                        if len(self.wait.queue) <= 0:
                            break

            self.systemClock.increment()
            self.ready.incrememnt(what='runtime')
            self.wait.incrememnt(what='waittime')
            self.readData()

    def PB(self):

        while self.haveProcesses():
            index = 0

            self.richTable.show_tables(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)

            while index < len(self.new.queue):
                self.ready.addPCB(self.new.queue.pop(index))
                newPriority = self.ready.queue[-1].priority[1:]         
                for cpu in self.running:
                    if cpu.busy:
                        currentPriority = cpu.runningPCB.priority[1:]
                        if int(newPriority) < int(currentPriority):
                            newProcess = self.ready.queue.pop()
                            self.ready.addPCB(cpu.runningPCB)
                            cpu.removeProcess()
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{self.ready.queue[-1].pid} preempted")
                            cpu.loadProcess(newProcess)
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{cpu.runningPCB.pid} obtained CPU:{self.running.index(cpu)}")

            for cpu in self.running:
                if cpu.busy:
                    cpu.decrementCurrentProcess()
                    cpu.incrementExecutionTime()
                    kickedOffProcess = cpu.KickOff()
                    if kickedOffProcess:
                        kickedOffProcess.incrementBurstIndex()
                        if kickedOffProcess.currBurstIndex == len(kickedOffProcess.bursts):
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.setTAT(self.systemClock.getClock() - kickedOffProcess.getArrivalTime())
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} terminated:\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT} \nRWT = {kickedOffProcess.readyQueueTotalTime}\nIWT = {kickedOffProcess.waitQueueTotalTime }")
                        else:
                            self.wait.addPCB(kickedOffProcess)
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} moved to Waiting queue")

            for io in self.IOs:
                if io.busy:
                    io.incrementExecutionTime()
                    io.decrementCurrentProcess()
                    kickedOffProcess = io.KickOff()
                    if kickedOffProcess:
                        kickedOffProcess.incrementBurstIndex()
                        if kickedOffProcess.currBurstIndex == len(kickedOffProcess.bursts):
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.setTAT(self.systemClock.getClock() - kickedOffProcess.getArrivalTime())
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} terminated:\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT} \nRWT = {kickedOffProcess.readyQueueTotalTime}\nIWT = {kickedOffProcess.waitQueueTotalTime }")
                        else:
                            self.ready.addPCB(kickedOffProcess)
                            self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                            self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{kickedOffProcess.pid} moved to Ready queue")

            if len(self.ready.queue) > 0: 
                for cpu in self.running:
                    if not cpu.busy:
                        pi = 0
                        maxPriority = self.ready.queue[0].priority[1:]
                        for i in range(len(self.ready.queue)):
                            newPriority = self.ready.queue[i].priority[1:]
                            if int(maxPriority) > int(newPriority):
                                pi = i
                                maxPriority = newPriority
                        cpu.loadProcess(self.ready.queue.pop(pi))
                        self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                        self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{cpu.runningPCB.pid} obtained CPU:{self.running.index(cpu)}")
                        if len(self.ready.queue) <= 0:
                            break

            if len(self.wait.queue) > 0:
                for io in self.IOs:
                    if not io.busy:
                        io.loadProcess(self.wait.removePCB())
                        self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)
                        self.richTable.show_message(f"At t:{self.systemClock.getClock()} job p{io.runningPCB.pid} obtained device:{self.IOs.index(io)}")
                        if len(self.wait.queue) <= 0:
                            break
            
            self.systemClock.increment()
            self.ready.incrememnt(what='runtime')
            self.wait.incrememnt(what='waittime')
            self.readData()
            
    def showResult(self):
        self.richTable.update(self.new.queue, self.ready.queue, [cpu.runningPCB for cpu in self.running if cpu.runningPCB is not None], self.wait.queue, [io.runningPCB for io in self.IOs if io.runningPCB is not None], self.terminated.queue)

        self.richTable.show_message(f"CPU Utilization: {sum([cpu.totalExecutionTime for cpu in self.running])*100/(self.systemClock.getClock() * len(self.running))}\nIO Utilization: {sum([cpu.totalExecutionTime for cpu in self.IOs])*100/(self.systemClock.getClock() * len(self.IOs))} \nAverage Turnaround Time: {sum([p.TAT for p in self.terminated.queue])/len(self.terminated.queue)} \nAverage Wait Time: {sum([p.readyQueueTotalTime for p in self.terminated.queue])/len(self.terminated.queue)} \nAverage I/O Wait Time: {sum([p.waitQueueTotalTime for p in self.terminated.queue])/len(self.terminated.queue)}")

    
    def start(self, algorithm):
        self.readData()
        if algorithm == 'FCFS':
            self.FCFS()
        elif algorithm == 'RR':
            self.RR()
        elif algorithm == 'PB':
            self.PB()
        else:
            print("Invalid algorithm")
            quit()
        self.showResult()    
        

if __name__ == '__main__':
    try:
        attrs = {}
        # parse command line arguments
        for i in range(1, len(sys.argv)):
            attr, value = sys.argv[i].split('=')
            attrs[attr] = value
        if len(attrs) < 4:
            raise Exception("Invalid number of arguments")
        if attrs['sched'] == "RR" and 'timeslice' not in attrs:
            raise Exception("Time slice missing")
        if attrs['sched'] not in ['FCFS', 'RR', 'PB']:
            raise Exception("Invalid Algorithm")

    except Exception as e:
        print(e)
        print("python sim.py sched=RR timeslice=3 cpus=4 ios=6 input=filename.dat")
        print("or")
        print("python sim.py sched=FCFS cpus=2 ios=2 input=otherfile.dat")
        print("Algorithms:")
        print("FCSF: First Come First Serve")
        print("RR: Round Robin")
        print("PB: Priority Based")
        quit()


    sim = Simulator(attrs['input'], int(attrs['cpus']), int(attrs['ios']), attrs.get('timeslice', None))
    sim.start(attrs['sched'])

    