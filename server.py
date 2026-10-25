import socket
import threading

HOST = ''
PORT = 50013

active = True
usernames = []

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
            print("ACCEPTED USERNAME:", username)
            usernames.append(username)

            conn.send("accepted".encode('utf-8'))
            break
        else:
            print("DENIED USERNAME", username, "(ALREADY EXISTS)")
            conn.send("denied".encode('utf-8'))

    print(f"{addr} has disconnected.")
    conn.close()

    if(threading.active_count() - 2 == 0):
        end = input("No active connections. Close server? [y/n] ")
        if end.lower() == 'y' or end.lower() == 'yes':
            global active
            active = False

def isUniqueUsername(username : str) -> bool:
    print("username count:", usernames.count(username))
    return usernames.count(username) == 0

if __name__ == "__main__":
    startServer()