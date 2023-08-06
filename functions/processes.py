import psutil
import subprocess, signal
import os

def getProcessList():
    """Returns a list of all running processes on the system.

    Returns:
        List: A list of dictionaries containing the process id, name, and number of threads.
    """
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'num_threads']):
        try:
            process_info = {
                'pid': proc.pid,
                'name': proc.name,
                'threads': proc.num_threads
            }
            process_list.append(process_info)
        except psutil.NoSuchProcess:
            pass
    return process_list 

def killProcess(pid):
    """Kills a process with the given pid.

    Args:
        pid (int): The process id of the process to kill.

    Returns:
        boolean: True if the process was killed, False otherwise.
    """
    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except:
        return False

def startProcess(process_name):
    """Starts a process with the given name. Note: Dont need to provide the full path to the process if it is in the system path.

    Args:
        process_name (string): The name/path of the process to start.

    Returns:
        boolean: True if the process was started, False otherwise.
    """    
    try:
        subprocess.Popen(process_name, shell=True)
        return True
    except:
        return False