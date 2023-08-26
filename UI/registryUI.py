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

def addToLog(log, text):
    log.config(state = "normal")
    log.insert("end", text)
    log.config(state = "disabled")

def setLog(log, text):
    log.config(state = "normal")
    log.delete("1.0", "end")
    log.insert("end", text)
    log.config(state = "disabled")

def clearLog(log):
    log.config(state = "normal")
    log.delete("1.0", "end")
    log.config(state = "disabled")

def hideLabel(nameLabel, nameTextbox, valueLabel, valueTextbox, datatypeLabel, datatypeBox):
    nameLabel.grid_forget()
    nameTextbox.grid_forget()
    valueLabel.grid_forget()
    valueTextbox.grid_forget()
    datatypeLabel.grid_forget()
    datatypeBox.grid_forget()

def showName(nameLabel, nameTextbox):
    nameLabel.grid(row = 3, column = 1, columnspan = 3, sticky = "w")
    nameTextbox.grid(row = 3, column = 4, columnspan = 10, sticky = "ew")
def showValue(valueLabel, valueTextbox):
    valueLabel.grid(row = 4, column = 1, columnspan = 3, sticky = "w", pady = 1)
    valueTextbox.grid(row = 4, column = 4, columnspan = 10, sticky = "ew", pady = 1)
def showType(datatypeLabel, datatypeBox):
    datatypeLabel.grid(row = 5, column = 1, columnspan = 3, sticky = "w", pady = 1)
    datatypeBox.grid(row = 5, column = 4, columnspan = 10, sticky = "ew", pady = 1)

def labelControl(functionBox, nameLabel, nameTextbox, valueLabel, valueTextbox, datatypeLabel, datatypeBox, event):
    option = functionBox.get()
    hideLabel(nameLabel, nameTextbox, valueLabel, valueTextbox, datatypeLabel, datatypeBox)
    if option == "Get value":
        showName(nameLabel, nameTextbox)
    elif option == "Set value":
        showName(nameLabel, nameTextbox)
        showValue(valueLabel, valueTextbox)
        showType(datatypeLabel, datatypeBox)

def request(functionBox, directoryBox, nameTextbox, valueTextbox, datatypeBox, log):
    option = functionBox.get()
    dir = directoryBox.get()
    cc.send("!REGISTRY")
    if option == "Get value":
        name = nameTextbox.get()
        cmd = "GETVAL," + dir + "," + name
        cc.send(cmd)
        data = cc.receive()
        if data == False:
            addToLog(log, "Fail to receive value\n")
        else:
            addToLog(log, data + "\n")
            
def prototype():
    popup = tk.Toplevel()
    popup.title("Fix Registry")
    popup_width = 408
    popup_height = 330 
    popup.geometry(f"{popup_width}x{popup_height}")

    emptyLabelsCol = []
    emptyLabelsRow = []
    # labelString = "label"
    for i in range(30):
        cur_label = tk.Label(popup, height = 1, width = 3, text = "")
        emptyLabelsCol.append(cur_label)
        cur_label.grid(row = 0, column = i)
    for i in range(20):
        cur_label = tk.Label(popup, height = 1, width = 1, text = "")
        emptyLabelsRow.append(cur_label)
        cur_label.grid(row = i, column = 0)
    
    
    nameLabelText = "Name:"
    nameLabel = tk.Label(popup, text = nameLabelText)
    nameTextBox = tk.Entry(popup, highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    
    valueLabelText = "Value:"
    valueLabel = tk.Label(popup, text = valueLabelText)
    valueTextBox = tk.Entry(popup, highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    
    datatypeText = "Data Type:"
    dataLabel = tk.Label(popup, text = datatypeText)
    datatypeBox = ttk.Combobox(popup, values = ["Choose", "String", "DWORD", "QWORD", "Multi-String", "Expandable-String"], state = "readonly")
    datatypeBox.set("Choose")
    
    nameLabel.grid_forget()
    nameTextBox.grid_forget()
    valueLabel.grid_forget()
    valueTextBox.grid_forget()
    dataLabel.grid_forget()
    datatypeBox.grid_forget()

    functionBox = ttk.Combobox(popup, values = ["Choose", "Get value", "Set value", "Delete value", "Create key", "Delete key"], state = "readonly")
    functionBox.grid(row = 1, column = 1, columnspan = 13, sticky = "ew")
    functionBox.set("Choose")

    functionBox.bind("<<ComboboxSelected>>", partial(labelControl, functionBox, nameLabel, nameTextBox, valueLabel, valueTextBox, dataLabel, datatypeBox))

    # emptyLabel_b = tk.Label(popup, width = 1, height = 1)
    # emptyLabel_b.grid(row = 2, column = 1)

    directoryText = "Directory:"
    directoryLabel = tk.Label(popup, text = directoryText, pady = 2)
    directoryLabel.grid(row = 2, column = 1, columnspan = 3, sticky = "w", pady = 2)
    directoryBox = tk.Entry(popup, highlightbackground = "black", highlightcolor = "black", highlightthickness = 1)
    directoryBox.grid(row = 2, column = 4, columnspan = 10, pady = 2, sticky = "ew")

    logLabel = tk.Label(popup, text = "Log:")
    logLabel.grid(row = 6, column = 1, columnspan = 3, sticky = "w", pady = 2)
    
    logtext = tk.Text(popup, width = 40, height = 7, wrap = "word", highlightbackground = "gray", highlightcolor = "gray", background = "gray90", highlightthickness = 1, state = "disabled")
    # logtext = tk.Text(popup, width = 40, height = 7, wrap = "word", highlightbackground = "gray", highlightcolor = "gray", highlightthickness = 1, state = "disabled")
    logtext.grid(row = 7, column = 1, columnspan = 13, sticky = "nsew", pady = 2)
    
    sendButton = tk.Button(popup, text = "Request")
    sendButton.grid(row = 8, column = 6, columnspan = 3, sticky = "ew", pady = 5)

    popup.mainloop()

# prototype() 
