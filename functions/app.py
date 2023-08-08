import subprocess
import win32gui
import re

def getAppList():
    """Returns a list of all running applications on the system.

    Returns:
        list: A list of dictionaries containing the application description, id, path, and number of threads.
    """
    
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,Path,@{Name=\'Threads\';Expression={(Get-Process -Id $_.Id).Threads.Count}}"'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    process_list = []

    for line in proc.stdout.readlines():
        # print(repr(line))
        if not line.decode().isspace():
            try:
                input_string = line.decode()
                # print(input_string)

                # Define a regular expression pattern to match the information
                pattern = r'(.+?)\s+(\d+)\s+(.+)\s+(\d+)'

                # Use the regular expression to match the pattern in the input string
                match = re.match(pattern, input_string)

                if match:
                    description = match.group(1)
                    app_id = match.group(2)
                    path = match.group(3)
                    threads = match.group(4)
                    
                    result_list = [description.strip(), app_id, path.strip(), threads]
                    
                    process_list.append(result_list)
                    # print(result_list)
            except:
                pass    
    return process_list     
    
def killApp(app_id):
    """Kills an application based on the application id.

    Args:
        app_id (int): The application id.
    """
    cmd = 'powershell "Stop-Process -Id ' + str(app_id) + '"'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    proc.wait()
    # print(proc.stdout.read())
    
    
for i in getAppList():
    print(i)

killApp(int(input("Enter the app id to kill: ")))





