import socket

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = str(len(message)).encode(FORMAT) 
    msg_len += (b' '*(HEADER - len(msg_len)))
    client.send(msg_len)
    client.send(message)

send("sapnu puas")
