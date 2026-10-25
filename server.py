import socket
import threading

HOST = ''
PORT = 50013

active = True
clients = []

def startServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    try:
        s.bind((HOST, PORT))
    except socket.error:
        print(f"Binding to {HOST}:{PORT} failed: {socket.error}")
        return

    s.listen(1)
    s.setblocking(False)
    print(f"Server started @ {HOST}:{PORT}")

    while active:
        try:
            conn, addr = s.accept()
            
            thread = threading.Thread(target=handleClient, args=(conn, addr))
            thread.daemon = True
            thread.start()

            print(f"{threading.active_count() - 1} active connections")
        except BlockingIOError:
            pass

def handleClient(conn, addr):
    print(f"New Connection @ {addr}")
    connected = True

    while True:
        #get client username
        data = conn.recv(1024)

        username = data.decode('utf-8')
        if (isUniqueUsername(username)):
            #print("ACCEPTED USERNAME:", username)
            clients.append((username, conn))

            conn.send("accepted".encode('utf-8'))
            broadcast(f"{username} joined.", username)
            break
        else:
            #print("DENIED USERNAME", username, "(ALREADY EXISTS)")
            conn.send("denied".encode('utf-8'))

    while connected:
        #messaging loop
        data = conn.recv(1024)
        if not data:
            break

        message = data.decode('utf-8')

        if message == "EXIT":
            connected = False
        else:
            broadcast(f"{username}> {message}", username)

    disconnectClient(username, conn)

    if(threading.active_count() - 2 == 0):
        end = input("No active connections. Close server? [y/n] ")
        if end.lower() == 'y' or end.lower() == 'yes':
            global active
            active = False

def broadcast(message, sender):
    for client in clients:
        if not client[0] == sender:
            #print(f"Sender: {client[0]}, Socket: {client[1]}")
            client[1].send(message.encode('utf-8'))

def disconnectClient(username, conn):
    #send disconnect message to all
    broadcast(f"{username} left.", username)
    print(f"{username} has disconnected.")

    clients.remove((username, conn))
    conn.close()

def isUniqueUsername(username : str) -> bool:
    for client in clients:
        if client[0] == username:
            return False
    return True
 
if __name__ == "__main__":
    startServer()