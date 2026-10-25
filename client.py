import socket
import threading
import sys

HOST = ''
PORT = 50013

active = True

def receive(user, s):
    global active

    while active:
        data = s.recv(1024)
        message = data.decode('utf-8')

        sys.stdout.flush()
        sys.stdout.write('\033[2K\033[1G')
        sys.stdout.flush()
        print(message, end='', flush=True)
        sys.stdout.write('\033[E')
        sys.stdout.flush()
        print(f"{user}> ", end='', flush=True)

def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((HOST, PORT))
        print(f"Connected to server @ {HOST}:{PORT}")
    except ConnectionRefusedError:
        print("Failed to connect to server.")
        return

    response = ''
    username = ''
    while not response == 'accepted':
        #ask for username
        username = input("Enter username: ")

        if not username.strip():
            continue

        try:
            #send to server
            s.send(username.encode('utf-8'))

            #server sends back status telling if its unique
            response = s.recv(1024).decode('utf-8')

            if response == 'denied':
                print("Username already taken. Please choose a different name.")
            #loop again if not unique

        except Exception:
            print(f"Connection to {HOST}:{PORT} failed: {Exception}")
            break

    #procede to message loop
    #thread for listening to incoming messages and server alerts
    thread = threading.Thread(target=receive, args=(username, s))
    thread.daemon = True
    thread.start()

    while True:
        message = input(f"{username}> ")
        s.send(message.encode('utf-8'))

        if message == 'EXIT':
            break

    global active
    active = False
    s.close()

if __name__ == "__main__":
    start()