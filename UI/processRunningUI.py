import tkinter as tk
from client import connect as cc

def prototype():
    popup = tk.Toplevel()
    popup.title("App running")
    popup_width = 400
    popup_height = 400
    popup.geometry(f"{popup_width}x{popup_height}")

    labelString = "label"

    emptyLabelsCol = []
    emptyLabelsRow = []

    for i in range(14):
        cur_label = tk.Label(popup, height = 1, width = 3, text = labelString)
        emptyLabelsCol.append(cur_label)
        cur_label.grid(row = 0, column = i)
    for i in range(16):
        cur_label = tk.Label(popup, height = 1, width = 1, text = f"{i}")
        emptyLabelsRow.append(cur_label)
        cur_label.grid(row = i, column = 0)

    killButton = tk.Button(popup, text = "Kill", height = 3)
    killButton.grid(row = 1, column = 1, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
    viewButton = tk.Button(popup, text = "View", height = 3)
    viewButton.grid(row = 1, column = 4, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
    eraseButton = tk.Button(popup, text = "Erase", height = 3)
    eraseButton.grid(row = 1, column = 7, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
    startButton = tk.Button(popup, text = "Start", height = 3)
    startButton.grid(row = 1, column = 10, columnspan = 3, sticky = "ew", padx = 6, pady = 5)

    # emptyLabel_b = tk.Label(popup, width = 1)
    # emptyLabel_b.grid(row = 2)

    textFrame = tk.Frame(popup, bg = "white", highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    textFrame = textFrame.grid(row = 3, column = 1, columnspan = 12, rowspan = 20, sticky = "nsew")
    titleFrame = tk.Frame(popup, bg = "white", highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    titleFrame = titleFrame.grid(row = 3, column = 1, columnspan = 12, rowspan = 1, sticky = "nsew")

    nameProcess = "Process Name"
    IDProcess = "Process ID"
    countThread = "Count Thread"
    
    titleAppLabel = tk.Label(popup, text = nameProcess, bg="white")
    titleAppLabel.grid(row = 3, column = 1, columnspan = 4, sticky = "w", padx = 1, pady = 1)
    IDLabel = tk.Label(popup, text = IDProcess, bg="white")
    IDLabel.grid(row = 3, column = 5, columnspan = 4, sticky = "w", padx = 1, pady = 1)
    threadLabel = tk.Label(popup, text = countThread, bg="white")
    threadLabel.grid(row = 3, column = 9, columnspan = 4, sticky = "w", padx = 1, pady = 1)

    appList = cc.receiveAppList()

    popup.mainloop()

prototype() 
