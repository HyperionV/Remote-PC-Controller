from functools import partial
import tkinter as tk
from tkinter import ttk
from tkinter import Text
from tkinter import messagebox
import sys
sys.path.append('../')
from client import connect as cc

global state
state = False

def hook():
    global state
    if state == False:
        print("state is now true\n")
        state = True
        cc.send("!KEYLOG")

def unhook(keystroke, canvas, textFrame):
    global state
    if state == True:
        state = False
        print("state is now false\n")
        cc.send("!KEYLOG")
        receiveKeystroke = cc.receive()
        # print(receiveKeystroke, "\n")
        keystroke.config(state="normal")
        keystroke.insert(tk.END, receiveKeystroke)
        keystroke.config(state="disabled")
        updateCanvas(canvas, textFrame)

# def print(textFrame, keystroke):

# def printKeystroke(keystroke, textFrame):
    
def updateCanvas(canvas, textFrame):
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.update()
    textFrame.update()

def clearKeystroke(keystroke, canvas, textFrame):
    keystroke.config(state="normal")
    keystroke.delete(1.0, tk.END)
    keystroke.config(state="disabled")
    keystroke.update()
    updateCanvas(canvas, textFrame)
    return

def prototype():
    popup = tk.Toplevel()
    popup.title("Keystroke")
    popup_width = 378
    popup_height = 440
    popup.geometry(f"{popup_width}x{popup_height}")

    labelString = ""

    emptyLabelsCol = []
    emptyLabelsRow = []

    for i in range(14):
        cur_label = tk.Label(popup, height = 1, width = 3, text = labelString)
        emptyLabelsCol.append(cur_label)
        cur_label.grid(row = 0, column = i)
    for i in range(16):
        cur_label = tk.Label(popup, height = 1, width = 1, text = "")
        emptyLabelsRow.append(cur_label)
        cur_label.grid(row = i, column = 0)
    # emptyLabelsCol[0].update()
    # print(emptyLabelsCol[0].winfo_width())
    # Initialize style
    s = ttk.Style()
    # Create style used by default for all Frames
    s.configure('TFrame', background='white')

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(popup, relief = "solid", borderwidth = 1)
    frame_canvas.grid(row = 3, column = 1, columnspan = 12, rowspan = 14, sticky = "nsew")
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)

    # Add a canvas in that frame
    canvas = tk.Canvas(frame_canvas, bg="white")
    canvas.grid(row=0, column=0, sticky="news")

    # Link a scrollbar to the canvas
    vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)

    textFrame = ttk.Frame(canvas, borderwidth = 1, relief = "flat")
    textFrame.grid(row = 0, column = 0, columnspan = 12, rowspan = 13, sticky = "nsew")
    canvas.create_window((0, 0), window=textFrame, anchor='nw')

    keystroke = Text(textFrame, height = 21 * 10, width = 3 * 12, yscrollcommand = vsb.set)
    keystroke.grid(row = 0, column = 0)
    keystroke.config(state="disabled")
    keystroke.update()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.update()
    textFrame.update()
    updateCanvas(canvas, textFrame)

    buttonStyle = "groove"
    hookButton = tk.Button(popup, text = "Hook", height = 3, command = partial(hook), relief = buttonStyle)
    hookButton.grid(row = 1, column = 1, columnspan = 4, sticky = "ew", padx = 6, pady = 5)
    unhookButton = tk.Button(popup, text = "Unhook", height = 3, command = partial(unhook, keystroke, canvas, textFrame), relief = buttonStyle)
    unhookButton.grid(row = 1, column = 5, columnspan = 4, sticky = "ew", padx = 6, pady = 5)
    # printButton = tk.Button(popup, text = "Print", height = 3,relief = buttonStyle)
    # printButton.grid(row = 1, column = 7, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
    eraseButton = tk.Button(popup, text = "Erase", height = 3, command = partial(clearKeystroke, keystroke, canvas, textFrame), relief = buttonStyle)
    eraseButton.grid(row = 1, column = 9, columnspan = 4, sticky = "ew", padx = 6, pady = 5)

    # textFrame.update()
    # print(textFrame.winfo_height(), textFrame.winfo_width())
    # emptyLabelsCol[1].update()
    # print(emptyLabelsCol[1].winfo_height(), emptyLabelsCol[1].winfo_width())
    # emptyLabelsRow[1].update()
    # print(emptyLabelsRow[1].winfo_height(), emptyLabelsRow[1].winfo_width())


    popup.mainloop()

# prototype() 
