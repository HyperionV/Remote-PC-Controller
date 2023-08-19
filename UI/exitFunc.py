import tkinter as tk
import threading

def connect_to_ip():
    ip_address = ip_entry.get()
    result_label.config(text=f"Connecting to {ip_address}...")
    connect_button.config(state=tk.DISABLED)

    # Simulate a connection attempt (replace this with actual networking code)
    def simulate_connection():
        import time
        time.sleep(3)  # Simulate connecting for 3 seconds
        return True

    def on_connection_result(result):
        if result:
            result_label.config(text=f"Connected to {ip_address}")
        else:
            result_label.config(text=f"Failed to connect to {ip_address}")
        connect_button.config(state=tk.NORMAL)

    # Create a thread to simulate the connection
    connection_thread = threading.Thread(target=lambda: on_connection_result(simulate_connection()))
    connection_thread.start()

root = tk.Tk()
root.title("IP Connection Example")

ip_label = tk.Label(root, text="Enter IP Address:")
ip_label.pack()

ip_entry = tk.Entry(root)
ip_entry.pack()

connect_button = tk.Button(root, text="Connect", command = connect_to_ip)
connect_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
