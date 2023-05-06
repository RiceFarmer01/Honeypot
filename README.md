# Honeypot

A simple honeypot application built using Python and Tkinter.

## Description

This application listens on a specified IP address and port number, and simulates a fake shell or SSH banner when a connection is received. The user can also choose to enable a fake shell, which accepts commands and sends fake output back to the client.

## Installation

To run the application, you will need Python 3.x and the following modules installed:

- tkinter
- datetime

## Usage

1. Clone the repository
2. Open the command line and navigate to the project directory
3. Run `python gui.py` as admin to start the application
4. Enter the IP address and port number you wish to listen on (localhost:8080 in most cases)
5. Click the "Start" button to start the honeypot
6. To stop the honeypot, click the "Stop" button or close the window 

## Files

- `gui.py`: The main GUI for the application
- `honeypot.py`: The logic for the honeypot functionality
- `honeypot.log`: A log file that records all incoming connections and commands (if shell is enabled)

## Credits

Made by RiceFarmer01 aka Jaiden

## License

This project is licensed under the MIT License - see the LICENSE file for details.
