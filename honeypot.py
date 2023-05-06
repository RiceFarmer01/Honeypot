import tkinter as tk
from tkinter import ttk
from datetime import datetime
import socket

class Honeypot:
    def __init__(self, master):
        self.master = master
        self.master.title("Honeypot")
        self.master.geometry("300x250")
        self.master.configure(bg="#f0f0f0")

        # Create IP address label and entry box
        self.ip_label = ttk.Label(self.master, text="IP address:")
        self.ip_label.pack(pady=5)
        self.ip_entry = ttk.Entry(self.master)
        self.ip_entry.pack(pady=5)

        # Create port label and entry box
        self.port_label = ttk.Label(self.master, text="Port:")
        self.port_label.pack(pady=5)
        self.port_entry = ttk.Entry(self.master)
        self.port_entry.pack(pady=5)

        # Create fake shell checkbox
        self.shell_var = tk.BooleanVar()
        self.shell_check = ttk.Checkbutton(self.master, text="Enable fake shell", variable=self.shell_var)
        self.shell_check.pack(pady=5)

        # Create start button
        self.start_button = ttk.Button(self.master, text="Start", command=self.start_honeypot)
        self.start_button.pack(pady=10)

        # Create status label
        self.status_label = ttk.Label(self.master, text="Honeypot not running")
        self.status_label.pack(pady=5)

def start_honeypot(self):
    ip_address = self.ip_entry.get()
    port = int(self.port_entry.get())

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the IP address and port number
    server_socket.bind((ip_address, port))

    # Listen for incoming connections
    server_socket.listen(1)

    self.status_label.config(text=f"Honeypot listening on {ip_address}:{port}")

    # Accept incoming connections
    client_socket, client_address = server_socket.accept()

    self.status_label.config(text=f"Connection received from {client_address}")

    # Log connection information
    log_file = open("honeypot.log", "a")
    log_file.write(f"{datetime.now()} - Connection received from {client_address}\n")
    log_file.close()

    if self.shell_var.get():
        # Send a fake shell prompt to the client
        client_socket.send(b"Welcome to the honeypot shell!\n$ ")

        # Receive commands from the client and send fake output
        while True:
            command = client_socket.recv(1024).decode().strip()

            # Log command information
            log_file = open("honeypot.log", "a")
            log_file.write(f"{datetime.now()} - Command received from {client_address}: {command}\n")
            log_file.close()

            # Send fake output to the client
            output = b"Invalid command\n"
            if command == "ls":
                output = b"file1.txt  file2.txt\n"
            elif command == "cat file1.txt":
                output = b"This is file1\n"
            elif command == "cat file2.txt":
                output = b"This is file2\n"
            client_socket.send(output + b"$ ")
    else:
        # Send a fake banner to the client
        client_socket.send(b"SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.10\n")

    # Close the client socket
    client_socket.close()

    # Close the server socket
    server_socket.close()