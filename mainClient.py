import tkinter as tk
# import sys
# sys.path.append('../')
from client import connect as cc
from UI import appRunningUI as appui
from UI import processRunningUI as prui
from UI import keystrokeUI as ksui
from UI import registryUI as regui
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

def errorConnect():
    messagebox.showerror("Error", "Error connect to server")

def insert_IP():
    IP = str(textBox.get())
    # messagebox.showinfo("Notice", "Connecting to server ...")
    if cc.tryConnect(IP) == False:
        print("error connect\n")
        errorConnect()
        return
    else:
        connected = True
        messagebox.showinfo("Notice", "Connection established!")

def screenshot():
    cc.send(SCREENSHOT_MSG)
    screenshot_data = cc.receive_screenshot()
    cc.display_screenshot(screenshot_data)        

def exit_window():
    if(connected == True):
        cc.send(DISCONNECT_MSG)
        cc.client.close()
    root.destroy()
    return 0

def shutdown():
    cc.send(SHUTDOWN_MSG)

# def openAppRunningWindow():
#     popup = tk.Toplevel()
#     popup_width = 496
#     popup_height = 279
#     popup.geometry(f"{popup_width}x{popup_height}")

    # popup.mainloop()

root = tk.Tk()
root.title("Client")

window_width = 496 
window_height = 279 

root.geometry(f"{window_width}x{window_height}")

labelString = ""    

emptyLabel_a0 = tk.Label(root, height = 1, width = 8, text = labelString)
emptyLabel_a0.grid(row = 0, column = 0)
emptyLabel_a1 = tk.Label(root, height = 1, width = 8, text = labelString)
emptyLabel_a1.grid(row = 0, column = 1)
emptyLabel_a2 = tk.Label(root, height = 1, width = 8, text = labelString)
emptyLabel_a2.grid(row = 0, column = 2)
emptyLabel_a3 = tk.Label(root, height = 1, width = 8, text = labelString)
emptyLabel_a3.grid(row = 0, column = 3)
emptyLabel_a4 = tk.Label(root, height = 1, width = 8, text = labelString)
emptyLabel_a4.grid(row = 0, column = 4)
emptyLabel_a5 = tk.Label(root, height = 1, width = 8, text = labelString)
emptyLabel_a5.grid(row = 0, column = 5)
emptyLabel_a6 = tk.Label(root, height = 1, width = 8, text = labelString)
emptyLabel_a6.grid(row = 0, column = 6)
emptyLabel_a7 = tk.Label(root, height = 1, width = 8, text = labelString)
emptyLabel_a7.grid(row = 0, column = 7)

textBoxLabel = tk.Label(root, text = "Insert IP:")
textBoxLabel.grid(row = 1, column = 1)

textBox = tk.Entry(root)
textBox.grid(row = 1, column = 2, columnspan = 3, sticky = "ew")

connectButton = tk.Button(root, text = "Connect", command = insert_IP, height = 1)
connectButton.grid(row = 1, column = 5, columnspan = 2, sticky = "ew", padx = 4)

emptyLabel_c = tk.Label(root, width = 1)
emptyLabel_c.grid(row = 2)

appRunningButton = tk.Button(root, text = "App Running", command = appui.prototype, height = 3)
appRunningButton.grid(row = 3, column = 1, columnspan = 3, sticky = "ew", padx = 6)
processRunningButton = tk.Button(root, text = "Process Running", command = prui.prototype, height = 3)
processRunningButton.grid(row = 3, column = 4, columnspan = 3, sticky = "ew", padx = 6)

keystrokeButton = tk.Button(root, text = "Keystroke", command = ksui.prototype, height = 3)
keystrokeButton.grid(row = 5, column = 1, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
registryButton = tk.Button(root, text = "Fix registry", command = regui.prototype, height = 3)
registryButton.grid(row = 5, column = 4, columnspan = 3, sticky = "ew", padx = 6, pady = 5)

screenshotButton = tk.Button(root, text = "Screenshot", command = screenshot, height = 3)
screenshotButton.grid(row = 7, column = 1, columnspan = 2, sticky = "ew", padx = 6, pady = 5)
shutdownButton = tk.Button(root, text = "Shutdown", command = shutdown, height = 3)
shutdownButton.grid(row = 7, column = 3, columnspan = 2, sticky = "ew", padx = 6, pady = 5)
exitButton = tk.Button(root, text = "Exit", height = 3, command = exit_window)
exitButton.grid(row = 7, column = 5, columnspan = 2, sticky = "ew", padx = 6, pady = 5)

root.protocol("WM_DELETE_WINDOW", exit_window)
root.mainloop()