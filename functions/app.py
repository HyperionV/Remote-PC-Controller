import subprocess
import re

def getAppList():
    cmd = ['powershell', 'gps | where {$_.MainWindowTitle } | select Description,Id,Path,@{Name=\'Threads\';Expression={(Get-Process -Id $_.Id).Threads.Count}}']
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)
        process_list = []
        
        for line in proc.stdout.splitlines():
            line = line.strip()
            print(line)

            # Define a regular expression pattern to match the information
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
                    print("No match found in the input string.")
        
        return process_list
    
    except subprocess.CalledProcessError as e:
        print("Error executing PowerShell command:", e)

def killApp(app_id):
    cmd = f'powershell "Stop-Process -Id {app_id}"'
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error executing PowerShell command:", e)

if __name__ == "__main__":
    app_list = getAppList()
    for app in app_list:
        print(app)
    
    try:
        app_id_to_kill = int(input("Enter the app id to kill: "))
        killApp(app_id_to_kill)
    except ValueError:
        print("Invalid input. Please enter a valid numeric app id.")
