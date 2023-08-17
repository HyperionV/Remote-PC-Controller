import tkinter as tk
import processRunningUI

def on_button_click():
    entered_text = textBox.get()
    print("Entered text:", entered_text)

def exit_window():
    root.destroy()
    return 0
    
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

connectButton = tk.Button(root, text = "Connect", command = on_button_click, height = 1)
connectButton.grid(row = 1, column = 5, columnspan = 2, sticky = "ew", padx = 4)

emptyLabel_c = tk.Label(root, width = 1)
emptyLabel_c.grid(row = 2)

appRunningButton = tk.Button(root, text = "App Running", height = 3)
appRunningButton.grid(row = 3, column = 1, columnspan = 3, sticky = "ew", padx = 6)
processRunningButton = tk.Button(root, text = "Process Running", height = 3)
processRunningButton.grid(row = 3, column = 4, columnspan = 3, sticky = "ew", padx = 6)

keystrokeButton = tk.Button(root, text = "Keystroke", height = 3)
keystrokeButton.grid(row = 5, column = 1, columnspan = 3, sticky = "ew", padx = 6, pady = 5)
registryButton = tk.Button(root, text = "Fix registry", height = 3)
registryButton.grid(row = 5, column = 4, columnspan = 3, sticky = "ew", padx = 6, pady = 5)

screenshotButton = tk.Button(root, text = "Screenshot", height = 3)
screenshotButton.grid(row = 7, column = 1, columnspan = 2, sticky = "ew", padx = 6, pady = 5)
shutdownButton = tk.Button(root, text = "Shutdown", height = 3)
shutdownButton.grid(row = 7, column = 3, columnspan = 2, sticky = "ew", padx = 6, pady = 5)
exitButton = tk.Button(root, text = "Exit", height = 3, command = exit_window)
exitButton.grid(row = 7, column = 5, columnspan = 2, sticky = "ew", padx = 6, pady = 5)

root.mainloop()