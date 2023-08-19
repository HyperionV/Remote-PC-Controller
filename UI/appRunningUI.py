from functools import partial
import tkinter as tk
from tkinter import ttk
import sys
sys.path.append('../')
from client import connect as cc

def resizeLabel(label, width):
    label.update()
    if(label.winfo_width() <= width):
        return
    while(label.winfo_width() > width):
        text = label.cget("text")
        label.config(text = text[:-1])
        label.update()
    text = label.cget("text")
    label.config(text = text[:-3] + "...")
    label.update()

def getAppList(textFrame, appLabel):
    cc.send("!GETAPP")
    appList = cc.receiveAppList()
    cnt = 0
    # emptyLabel = tk.Label(textFrame, height = 1)
    # emptyLabel.grid(row = 0)

    emptyLabelsCol = []
    labelString = ""
    for i in range(1, 10):
        cur_label = tk.Label(textFrame, height = 1, width = 3, text = labelString, bg = "white")
        emptyLabelsCol.append(cur_label)
        cur_label.grid(row = 0, column = i)

    for app in appList:
        description = app['description']
        appID = app['app_id']
        thread = app['thread']

        curLabelName = tk.Label(textFrame, text = description, bg = "white")
        curLabelName.grid(row = cnt, column = 0, sticky = "w")
        resizeLabel(curLabelName, 30*4)
        curLabelID = tk.Label(textFrame, text = appID, bg = "white")
        curLabelID.grid(row = cnt, column = 1, columnspan = 4, sticky = "w")
        resizeLabel(curLabelID, 30*4)
        curLabelThread = tk.Label(textFrame, text = thread, bg = "white")
        curLabelThread.grid(row = cnt, column = 5, columnspan = 4, sticky = "w")
        resizeLabel(curLabelThread, 30*4)

        curLabel = []
        curLabel.append(curLabelName)
        # curLabel.append(curLabelID)
        # curLabel.append(curLabelThread)
        appLabel.append(curLabel)
        
        cnt = cnt + 1

def prototype():
    print("owo")
    appLabel = []
    popup = tk.Toplevel()
    popup.title("App running")
    popup_width = 378
    popup_height = 440
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
    emptyLabelsCol[0].update()
    print(emptyLabelsCol[0].winfo_width())
    # Initialize style
    s = ttk.Style()
    # Create style used by default for all Frames
    s.configure('TFrame', background='white')

    # emptyLabel_b = tk.Label(popup, width = 1)
    # emptyLabel_b.grid(row = 2)

    # textFrame = tk.Frame(popup, bg = "white", highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    # textFrame = textFrame.grid(row = 3, column = 1, columnspan = 12, rowspan = 15, sticky = "nsew")

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(popup)
    frame_canvas.grid(row = 4, column = 1, columnspan = 12, rowspan = 13, sticky = "nsew")
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)

    # Add a canvas in that frame
    canvas = tk.Canvas(frame_canvas, bg="yellow")
    canvas.grid(row=0, column=0, sticky="news")

    # Link a scrollbar to the canvas
    vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)

    textFrame = ttk.Frame(canvas, borderwidth = 1, relief = "solid")
    textFrame.grid(row = 0, column = 0, columnspan = 12, rowspan = 13, sticky = "nsew")
    canvas.create_window((0, 0), window=textFrame, anchor='nw')
    
    
    titleFrame = tk.Frame(popup, bg = "white", highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    titleFrame.grid(row = 3, column = 1, columnspan = 12, rowspan = 1, sticky = "nsew")
    

    # titleFrame = ttk.Frame(popup, borderwidth = 1, relief="solid")
    # titleFrame.grid(row = 3, column = 1, columnspan = 12, rowspan = 1, sticky = "nsew")

    buttonStyle = "groove"
    killButton = tk.Button(popup, text = "Kill", height = 3, relief = buttonStyle)
    killButton.grid(row = 1, column = 1, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
    viewButton = tk.Button(popup, text = "View", height = 3, command = partial(getAppList, textFrame, appLabel), relief = buttonStyle)
    viewButton.grid(row = 1, column = 4, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
    eraseButton = tk.Button(popup, text = "Erase", height = 3, relief = buttonStyle)
    eraseButton.grid(row = 1, column = 7, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
    startButton = tk.Button(popup, text = "Start", height = 3, relief = buttonStyle)
    startButton.grid(row = 1, column = 10, columnspan = 3, sticky = "ew", padx = 6, pady = 5)

    nameApp = "Application Name"
    IDApp = "Application ID"
    countThread = "Count Thread"
    
    titleAppLabel = tk.Label(popup, text = nameApp, bg="white")
    titleAppLabel.grid(row = 3, column = 1, columnspan = 4, sticky = "w", padx = 1, pady = 1)
    IDLabel = tk.Label(popup, text = IDApp, bg="white")
    IDLabel.grid(row = 3, column = 5, columnspan = 4, sticky = "w", padx = 1, pady = 1)
    threadLabel = tk.Label(popup, text = countThread, bg="white")
    threadLabel.grid(row = 3, column = 9, columnspan = 4, sticky = "w", padx = 1, pady = 1)


    popup.mainloop()

# prototype() 
