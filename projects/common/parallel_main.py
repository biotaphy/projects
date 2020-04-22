"""Parallel script for getting things done."""
from subprocess import Popen, PIPE
from time import sleep, time

CONCURRENT_PROCESSES = 20
WAIT_TIME = .1

# .............................................................................
def get_species_list_from_file(filename):
    species_names = []
    with open(filename) as in_file:
        for line in in_file:
            try:
                parts = line.split(',')
                species_names.append(parts[1].strip().strip('"'))
            except Exception as err:
                print(err)
    return species_names

# .............................................................................
class SubprocessManager(object):
    """This class manages subprocesses
    """
    # .............................
    def __init__(self, commandList=[], maxConcurrent=CONCURRENT_PROCESSES):
        """
        Args:
            * commandList: A list of commands to run as subprocesses
            * maxConcurrent: (optional) The maximum number of subprocesses to 
                run concurrently
        """
        self.procs = commandList
        self.maxConcurrent = maxConcurrent
        self._runningProcs = []
    
    # .............................
    def addProcessCommands(self, commandList):
        """Adds a list of commands to the list to run 
        """
        self.procs.extend(commandList)
    
    # .............................
    def runProcesses(self):
        """Runs the processes in self.procs
        """
        i = 0
        one_tenth = int(len(self.procs) / 1000)
        start_time = time()
        percent = 0.0
        while len(self.procs) > 0:
            numRunning = self.getNumberOfRunningProcesses()
            num = min((self.maxConcurrent - numRunning), len(self.procs))
            
            while num > 0:
                proc = self.procs.pop(0)
                self.launchProcess(proc)
                num = num - 1
                i += 1
                if i % one_tenth == 0:
                    percent += .1
                    print('{}%, {} seconds'.format(percent, time() - start_time))
            
            self.wait()
        
        while self.getNumberOfRunningProcesses() > 0:
            self.wait()
        
    # .............................
    def wait(self, waitSeconds=WAIT_TIME):
        """Waits the specified amount of time
        """
        sleep(waitSeconds)
    
    # .............................
    def launchProcess(self, cmd):
        """Launches a subprocess for the command provided
        """
        self._runningProcs.append(Popen(cmd, shell=True))
    
    # .............................
    def getNumberOfRunningProcesses(self):
        """Returns the number of running processes
        """
        numRunning = 0
        for idx in xrange(len(self._runningProcs)):
            if self._runningProcs[idx].poll() is None:
                numRunning = numRunning +1
            else:
                self._runningProcs[idx] = None
        self._runningProcs = filter(None, self._runningProcs)
        return numRunning

# .............................................................................
def main():
    """main method."""
    # Get list of species
    species_filename = '/DATA/biotaphy/seed_plants/accepted_species.csv'
    species_names = get_species_list_from_file(species_filename) # [:10000]
    sp_commands = ['python /home/cjgrady/git/projects/projects/common/get_points_for_species.py "{}"'.format(sp) for sp in species_names]
    # Create a pool of processes
    spm = SubprocessManager(commandList=sp_commands)
    # Start processes
    print('Running')
    spm.runProcesses()
    print('Done')
    # Add new as processes complete


# .............................................................................
if __name__ == '__main__':
    main()
