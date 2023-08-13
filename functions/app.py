import subprocess
import re

def getAppList():
    cmd = ['powershell', 'gps | where {$_.MainWindowTitle } | select Description,Id,Path,@{Name=\'Threads\';Expression={(Get-Process -Id $_.Id).Threads.Count}}']
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)
    process_list = []
    
    for line in proc.stdout.splitlines():
        line = line.strip()
        # print(line)
        pattern = r'(.+?)\s+(\d+)\s+(.+)\s+(\d+)'
        match = re.match(pattern, line)
        if line:
            if match:
                description = match.group(1)
                app_id = match.group(2)
                path = match.group(3)
                threads = match.group(4)
                
                result_dict = {
                    'description': description,
                    'app_id': app_id,
                    'path': path,
                    'threads': threads
                }
                process_list.append(result_dict)
            else:
                pass
    return (process_list, len(process_list))

def killApp(app_id):
    cmd = f'powershell "Stop-Process -Id {app_id}"'
    try:
        subprocess.run(cmd, shell=True, check=True)
        return f"App with ID {app_id} has been killed"
    except:
        return f"Error while killing app with ID {app_id}"
