import socket
import threading

HOST = '' # Listen on all available network interfaces
PORT = 12345

def handle_client(client_socket, client_address, clients):
    print(f'New connection from {client_address}')

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        print(f'Received message from {client_address}: {message}')

        broadcast(message, client_socket, clients)

    clients.remove(client_socket)
    client_socket.close()
    print(f'Client {client_address} disconnected')

def broadcast(message, sender_socket, clients):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode('utf-8'))
            except:
                clients.remove(client)
                client.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f'Server started on {HOST}:{PORT}')

    clients = []

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clients))
        thread.daemon = True
        thread.start()

        server_send_thread = threading.Thread(target=send_message, args=(client_socket,))
        server_send_thread.daemon = True
        server_send_thread.start()

def send_message(client_socket):
    while True:
        message = input()
        try:
            client_socket.sendall(message.encode('utf-8'))

        except:
            break

start_server()