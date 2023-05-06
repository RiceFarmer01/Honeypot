import socket
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class Honeypot:
    def __init__(self, master):
        self.master = master
        self.master.title("Honeypot")
        self.master.geometry("300x275")
        self.master.configure(bg="#f0f0f0")

        self.ip_label = ttk.Label(self.master, text="IP address:")
        self.ip_label.pack(pady=5)
        self.ip_entry = ttk.Entry(self.master)
        self.ip_entry.pack(pady=5)

        self.port_label = ttk.Label(self.master, text="Port:")
        self.port_label.pack(pady=5)
        self.port_entry = ttk.Entry(self.master)
        self.port_entry.pack(pady=5)

        self.shell_var = tk.BooleanVar()
        self.shell_check = ttk.Checkbutton(self.master, text="Enable fake shell", variable=self.shell_var)
        self.shell_check.pack(pady=5)

        self.start_button = ttk.Button(self.master, text="Start", command=self.start_honeypot)
        self.start_button.pack(pady=10)

        self.status_label = ttk.Label(self.master, text="Honeypot not running")
        self.status_label.pack(pady=5)

        self.frame = ttk.Frame(self.master)
        self.frame.pack(side=tk.TOP, pady=5)

        self.made_by_label = ttk.Label(self.frame, text="made by jaiden", foreground="#555", font=("TkDefaultFont", 8))
        self.made_by_label.pack(side=tk.LEFT, padx=5)

        self.link_label = tk.Label(self.frame, text="https://github.com/RiceFarmer01", foreground="#06f", cursor="hand2")
        self.link_label.pack(side=tk.LEFT, padx=5)
        self.link_label.bind("<Button-1>", lambda e: self.open_url("https://github.com/RiceFarmer01"))

    def start_honeypot(self):
        try:
            ip_address = self.ip_entry.get()
            port = int(self.port_entry.get())

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((ip_address, port))
            server_socket.listen(1)
            print(f"Server listening on {ip_address}:{port}")

            self.status_label.config(text=f"Honeypot listening on {ip_address}:{port}")
            self.master.update()  # Update the GUI

            client_socket, client_address = server_socket.accept()

            self.status_label.config(text=f"Connection received from {client_address}")

            log_file = open("honeypot.log", "a")
            log_file.write(f"{datetime.now()} - Connection received from {client_address}\n")
            log_file.close()

            if self.shell_var.get():
                client_socket.send(b"Welcome to the honeypot shell!\n$ ")

                while True:
                    command = client_socket.recv(1024).decode().strip()

                    log_file = open("honeypot.log", "a")
                    log_file.write(f"{datetime.now()} - Command received from {client_address}: {command}\n")
                    log_file.close()

                    output = b"Invalid command\n"
                    if command == "ls":
                        output = b"file1.txt  file2.txt\n"
                    elif command == "cat file1.txt":
                        output = b"This is file1\n"
                    elif command == "cat file2.txt":
                        output = b"This is file2\n"
                    client_socket.send(output + b"$ ")
            else:
                client_socket.send(b"SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.10\n")
                client_socket.recv(1024)

            client_socket.close()
            server_socket.close()
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred: {e}")

    def open_url(self, url):
        import webbrowser
        webbrowser.open_new(url)

root = tk.Tk()
honeypot = Honeypot(root)
root.mainloop()
