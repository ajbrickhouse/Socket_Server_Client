import socket
import threading
import PySimpleGUI as sg

# Constants
HOST = '127.0.0.1'
PORT = 12345

# Set up the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# PySimpleGUI layout
layout = [
    [sg.Text("Server Chat", size=(50, 1), justification="center")],
    [sg.Multiline(size=(50, 10), disabled=True, key="chat_log")],
    [sg.Input(size=(50, 1), key="input_box")],
    [sg.Button("Send", size=(35,1)), sg.Button("Exit", size=(5,1))],
]

window = sg.Window("Server Chat", layout, element_justification="center")

clients = []

def accept_clients():
    while True:
        client, address = server.accept()
        clients.append(client)
        message = f"Connected with {str(address)}"
        window["chat_log"].print(message)       
        client_thread = threading.Thread(target=receive, args=(client,))
        client_thread.start()

def receive(client):
    while True:
        try:
            # Receive message from client
            message = client.recv(1024).decode('utf-8')
            if message:
                window["chat_log"].print(f"Client {client.getpeername()}: {message}")
            else:
                break
        except socket.error:
            break

    window["chat_log"].print(f"Client {client.getpeername()} disconnected")
    client.close()
    clients.remove(client)

# Start accepting clients in a separate thread
accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()

# Event loop
while True:
    event, values = window.read()
    print("Event and Value: ", event, values)
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    elif event == "Send":
        message = values["input_box"]
        window["chat_log"].print(f"Server: {message}")
        for client in clients:
            try:
                client.send(message.encode('utf-8'))
            except socket.error:
                pass
        window["input_box"].update("")

server.close()
window.close()
