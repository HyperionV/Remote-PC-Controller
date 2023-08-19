import tkinter as tk
import threading
from client import connect

def connect_and_start_thread():
    connection_thread = threading.Thread()
    connection_thread.start()