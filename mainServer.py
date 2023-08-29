import tkinter as tk
import threading
# import sys
# sys.path.append('../')
from server import connect as sc
from UI import appRunningUI as appui
from UI import processRunningUI as prui
from UI import keystrokeUI as ksui
from UI import registryUI as regui
from functools import partial
from tkinter import messagebox

DISCONNECT_MSG = "!DISCONNECT"
SCREENSHOT_MSG = "!SCREENSHOT"
SHUTDOWN_MSG = "!SHUTDOWN"
KEYLOG_MSG = "!KEYLOG"
GETAPP_MSG = "!GETAPP"
KILLAPP_MSG = "!KILLAPP"
REGISTRY_MSG = "!REGISTRY"
PROCESS_MSG = "!PROCESS"

connected = False
IP = ""
thread = threading.Thread(target = sc.start)

def launch(textLabel):
    IP = sc.socket.gethostbyname(sc.socket.gethostname())
    thread.start()
    textLabel.config(text = "Server IP: " + IP)
    textLabel.grid(row = 1, column = 1, columnspan = 7, sticky = "w")

# def openAppRunningWindow():
#     popup = tk.Toplevel()
#     popup_width = 496
#     popup_height = 279
#     popup.geometry(f"{popup_width}x{popup_height}")

    # popup.mainloop()

root = tk.Tk()
root.title("Server")

window_width = 195
window_height = 120

root.geometry(f"{window_width}x{window_height}")

labelString = ""    

emptyLabel_a0 = tk.Label(root, height = 1, width = 2, text = labelString)
emptyLabel_a0.grid(row = 0, column = 0)
emptyLabel_a1 = tk.Label(root, height = 1, width = 2, text = labelString)
emptyLabel_a1.grid(row = 0, column = 1)
emptyLabel_a2 = tk.Label(root, height = 1, width = 2, text = labelString)
emptyLabel_a2.grid(row = 0, column = 2)
emptyLabel_a3 = tk.Label(root, height = 1, width = 2, text = labelString)
emptyLabel_a3.grid(row = 0, column = 3)
emptyLabel_a4 = tk.Label(root, height = 1, width = 2, text = labelString)
emptyLabel_a4.grid(row = 0, column = 4)
emptyLabel_a5 = tk.Label(root, height = 1, width = 2, text = labelString)
emptyLabel_a5.grid(row = 0, column = 5)
emptyLabel_a6 = tk.Label(root, height = 1, width = 2, text = labelString)
emptyLabel_a6.grid(row = 0, column = 6)
emptyLabel_a7 = tk.Label(root, height = 1, width = 2, text = labelString)
emptyLabel_a7.grid(row = 0, column = 7)

textLabel = tk.Label(root, text = "Server IP:")

emptyLabel_1 = tk.Label(root, width = 3)
emptyLabel_1.grid(row = 1, column = 0)

serverButton = tk.Button(root, text = "Launch server", command = partial(launch, textLabel), height = 2)
serverButton.grid(row = 2, column = 1, rowspan = 2, columnspan = 7, sticky = "ew", padx = 2)


root.mainloop()