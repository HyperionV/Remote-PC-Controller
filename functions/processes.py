import psutil
import subprocess, signal
import os

def getProcessList():
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'num_threads']):
        try:
            process_info = {
                'pid': proc.info['pid'], # type: ignore
                'name': proc.info['name'], # type: ignore
                'threads': proc.info['num_threads'] # type: ignore
            }
            process_list.append(process_info)
        except psutil.NoSuchProcess:
            pass
    return (process_list, len(process_list)) 

def killProcess(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except:
        return False

def startProcess(process_name):
    try:
        # Start the executable app in a non-blocking way
        subprocess.Popen([process_name])
        return True

    except FileNotFoundError:
        print(f"Could not find the executable at {process_name}")
        return False
