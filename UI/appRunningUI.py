from functools import partial
import tkinter as tk
from tkinter import ttk
import sys
sys.path.append('../')
from client import connect as cc

def getAppList(popup, appLabel):
    cc.send("!GETAPP")
    appList = cc.receiveAppList()
    cnt = 4
    for app in appList:
        description = app['description']
        appID = app['app_id']
        thread = app['thread']

        curLabelName = tk.Label(popup, text = description, bg = "white")
        curLabelName.grid(row = cnt, column = 1, columnspan = 4, sticky = "w", padx = 1, pady = 1)
        curLabelID = tk.Label(popup, text = appID, bg = "white")
        curLabelID.grid(row = cnt, column = 5, columnspan = 4, sticky = "w", padx = 1, pady = 1)
        curLabelThread = tk.Label(popup, text = thread, bg = "white")
        curLabelThread.grid(row = cnt, column = 9, columnspan = 4, sticky = "w", padx = 1, pady = 1)

        curLabel = []
        curLabel.append(curLabelName)
        curLabel.append(curLabelID)
        curLabel.append(curLabelThread)
        appLabel.append(curLabel)
        
        cnt = cnt + 1

def prototype():
    appLabel = []
    popup = tk.Toplevel()
    popup.title("App running")
    popup_width = 378
    popup_height = 400
    popup.geometry(f"{popup_width}x{popup_height}")

    labelString = ""

    emptyLabelsCol = []
    emptyLabelsRow = []

    for i in range(14):
        cur_label = tk.Label(popup, height = 1, width = 3, text = labelString)
        emptyLabelsCol.append(cur_label)
        cur_label.grid(row = 0, column = i)
    for i in range(16):
        cur_label = tk.Label(popup, height = 1, width = 1)
        emptyLabelsRow.append(cur_label)
        cur_label.grid(row = i, column = 0)

    # Initialize style
    s = ttk.Style()
    # Create style used by default for all Frames
    s.configure('TFrame', background='white')

    buttonStyle = "groove"
    killButton = tk.Button(popup, text = "Kill", height = 3, relief = buttonStyle)
    killButton.grid(row = 1, column = 1, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
    viewButton = tk.Button(popup, text = "View", height = 3, command = partial(getAppList, popup, appLabel), relief = buttonStyle)
    viewButton.grid(row = 1, column = 4, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
    eraseButton = tk.Button(popup, text = "Erase", height = 3, relief = buttonStyle)
    eraseButton.grid(row = 1, column = 7, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
    startButton = tk.Button(popup, text = "Start", height = 3, relief = buttonStyle)
    startButton.grid(row = 1, column = 10, columnspan = 3, sticky = "ew", padx = 6, pady = 5)

    # emptyLabel_b = tk.Label(popup, width = 1)
    # emptyLabel_b.grid(row = 2)

    # textFrame = tk.Frame(popup, bg = "white", highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    # textFrame = textFrame.grid(row = 3, column = 1, columnspan = 12, rowspan = 15, sticky = "nsew")
    # titleFrame = tk.Frame(popup, bg = "white", highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    # titleFrame = titleFrame.grid(row = 3, column = 1, columnspan = 12, rowspan = 1, sticky = "nsew")

   

    textFrame = ttk.Frame(popup, borderwidth = 1, relief = "solid")
    textFrame = textFrame.grid(row = 3, column = 1, columnspan = 12, rowspan = 13, sticky = "nsew")
    titleFrame = ttk.Frame(popup, borderwidth = 1, relief="solid")
    titleFrame = titleFrame.grid(row = 3, column = 1, columnspan = 12, rowspan = 1, sticky = "nsew")

    nameApp = "Application Name"
    IDApp = "Application ID"
    countThread = "Count Thread"
    
    titleAppLabel = tk.Label(popup, text = nameApp, bg="white")
    titleAppLabel.grid(row = 3, column = 1, columnspan = 4, sticky = "w", padx = 1, pady = 1)
    IDLabel = tk.Label(popup, text = IDApp, bg="white")
    IDLabel.grid(row = 3, column = 5, columnspan = 4, sticky = "w", padx = 1, pady = 1)
    threadLabel = tk.Label(popup, text = countThread, bg="white")
    threadLabel.grid(row = 3, column = 9, columnspan = 4, sticky = "w", padx = 1, pady = 1)

    # Create a scrollbar for the scrollable frame
    scrollbar = ttk.Scrollbar(textFrame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Configure the scrollbar to work with the scrollable frame
    # textFrame.configure(yscrollcommand=scrollbar.set)
    # scrollbar.config(command=textFrame.yview)

    popup.mainloop()

# prototype() 
