import socket
import threading
import PySimpleGUI as sg

# Constants
HOST = '127.0.0.1'
PORT = 12345

# Set up the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# PySimpleGUI layout
layout = [
    [sg.Text("Client Chat", size=(50, 1), justification="center")],
    [sg.Multiline(size=(50, 10), disabled=True, key="chat_log")],
    [sg.Input(size=(50, 1), key="input_box")],
    [sg.Button("Send", size=(35,1)), sg.Button("Exit", size=(5,1))],
]

window = sg.Window("Client Chat", layout, element_justification="center")

def receive():
    while True:
        try:
            # Receive a message from the server
            server_message = client.recv(1024).decode('utf-8')
            if server_message:
                window["chat_log"].print(f"Server: {server_message}")
            else:
                break
        except (socket.error, ConnectionAbortedError):
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Event loop
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break
    elif event == "Send":
        message = values["input_box"]
        window["chat_log"].print(f"Client: {message}")
        client.send(message.encode('utf-8'))
        window["input_box"].update("")

client.close()
window.close()
