import socket

HOST = ''
PORT = 50013

def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((HOST, PORT))
        print(f"Connected to server @ {HOST}:{PORT}")
    except ConnectionRefusedError:
        print("Failed to connect to server.")
        return

    response = ''
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
            print("SERVER:", response)
            #loop again if not unique

        except Exception:
            print(f"Connection to {HOST}:{PORT} failed: {Exception}")
            break

    #procede to message loop
    s.close()

if __name__ == "__main__":
    start()