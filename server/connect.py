import socket
import threading
# import pyautogui

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SCREENSHOT_MSG = "!SCREENSHOT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

def handle_client(connection, address):
    print(f"New connection initialized - {address}. ")
    # connected = True
    while True:
        msg_len = connection.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = connection.recv(msg_len).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                print(f"[{address}] - Connection closed")
                break
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
        # print(f"Active connections - {threading.active_count() - 1}")

print("Server is starting")
start()