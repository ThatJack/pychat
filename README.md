# Running the program (Linux)

* Ensure you have an up to date python version installed (at least Python 3)
* Run server.py first
* Run client.py (multiple times for multiple clients)

# Running the program (Windows)

* Ensure you have an up to date python version installed (at least Python 3)

#### Enable Virtual Terminal Processing:
1. open Powershell
2. input the following command: `Set-ItemProperty HKCU:\Console VirtualTerminalLevel -Type DWORD 1   `

* Run server.py first (Allow python through firewall)
* Run client.py (multiple times for multiple clients)

For an easier setup I recommend running on Linux.<br>

# Design Overview
### Server Side:

* Server opens socket connection and listens for connecting clients
* Each time a client connects, the server creates a new thread for handling that client
* Handling the client starts by listening for the client to send a username, checking for its uniqueness, and responding back whether it is accepted by the server
* Once accepted, the server broadcasts to all other connected users (if any) that a new user has joined and listens for messages from the client
* Upon hearing a message, the server broadcasts that message to all other connected clients in the form `username> message`
* If the message is exactly `EXIT`, the server closes the connection and instead broadcasts that the client has left the chat.

### Client Side:

* Client attempts to connect to the server (Ensure server is running before starting clients)
* Once connected, client prompts for a username, and sends it to the server
* If server denies username (not unique), prompt is repeated until an accepted name is entered
* Once a username is accepted, a new thread is created to listen to incoming messages from the server
* Main thread prompts for input until the user enters `EXIT` to disconnect
* Listening thread awaits receiving messages from the server
* Upon receiving a message, it overwrites the last console line to display the server's message, then rewrites the prompt for user input (This is why Virtual Processing/ANSI Escape Sequences must be enabled)
* Stops listening upon signal from main thread
