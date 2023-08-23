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

def onEntryClick(textBox, defaultText, event):
    if textBox.get() == defaultText:
        textBox.delete(0, tk.END) 
        textBox.config(fg = 'black')
        textBox.grid()

def onFocusOut(textBox, defaultText, event):
    if not textBox.get():
        textBox.insert(0, defaultText)  
        textBox.config(fg = 'gray')  

def labelControl(functionBox, popup, event):
    option = functionBox.get()
    nameTextBox = tk.Entry(popup, highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    nameTextBox.grid(row = 3, column = 1, columnspan = 3, sticky = "ew")
    defaultName = "Name"
    nameTextBox.bind("<FocusIn>", partial(onEntryClick, nameTextBox, defaultName))
    nameTextBox.bind("<FocusOut>", partial(onFocusOut, nameTextBox, defaultName))

    print("here?\n")
    # if option == "Get value":
        

def prototype():
    popup = tk.Toplevel()
    popup.title("Keystroke")
    popup_width = 408
    popup_height = 276 
    popup.geometry(f"{popup_width}x{popup_height}")

    emptyLabelsCol = []
    emptyLabelsRow = []
    # labelString = "label"
    for i in range(30):
        cur_label = tk.Label(popup, height = 1, width = 3, text = f"{i}")
        emptyLabelsCol.append(cur_label)
        cur_label.grid(row = 0, column = i)
    for i in range(20):
        cur_label = tk.Label(popup, height = 1, width = 1, text = f"{i}")
        emptyLabelsRow.append(cur_label)
        cur_label.grid(row = i, column = 0)

    functionBox = ttk.Combobox(popup, values = ["Choose", "Get value", "Set value", "Delete value", "Create key", "Delete key"], state = "readonly")
    functionBox.grid(row = 1, column = 1, columnspan = 13, sticky = "ew")
    functionBox.set("Choose")

    functionBox.bind("<<ComboboxSelected>>", partial(labelControl, functionBox, popup))

    # emptyLabel_b = tk.Label(popup, width = 1, height = 1)
    # emptyLabel_b.grid(row = 2, column = 1)

    directoryBox = tk.Entry(popup, highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    directoryBox.grid(row = 2, column = 1, columnspan = 13, pady = 4, sticky = "ew")

    popup.mainloop()

# prototype() 
