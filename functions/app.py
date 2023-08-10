import subprocess
import re

def getAppList():
    cmd = ['powershell', 'gps | where {$_.MainWindowTitle } | select Description,Id,Path,@{Name=\'Threads\';Expression={(Get-Process -Id $_.Id).Threads.Count}}']
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)
        process_list = []
        
        for line in proc.stdout.splitlines():
            line = line.strip()
            if line:
                try:
                    description, app_id, path, threads = re.split(r'\s+', line, maxsplit=3)
                    process_list.append({
                        'description': description,
                        'app_id': int(app_id),
                        'path': path,
                        'threads': int(threads)
                    })
                except Exception as e:
                    print(f"Error processing line: {line} - {e}")
        
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
    # for app in getAppList():
    #     print(app)
    
    try:
        app_id_to_kill = int(input("Enter the app id to kill: "))
        killApp(app_id_to_kill)
    except ValueError:
        print("Invalid input. Please enter a valid numeric app id.")
