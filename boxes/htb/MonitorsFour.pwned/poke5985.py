import socket

import os

# Configuration
TCP_IP = None  # The server's IP address (localhost for this example)
with open('./IP','r') as fh:
    TCP_IP=str(fh.readlines()[0])
TCP_PORT = 5985       # The port the server is listening on
BUFFER_SIZE = 1024    # Standard buffer size for receiving data
MESSAGE = b"Hello, World!" # Data must be in bytes

print(TCP_IP,TCP_PORT)

# 1. Create a socket object
# socket.AF_INET specifies the IPv4 address family
# socket.SOCK_STREAM specifies the TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect to the server
s.connect((TCP_IP, TCP_PORT))

# 3. Send data
s.send(MESSAGE)

# 4. Receive data from the server (optional)
data = s.recv(BUFFER_SIZE)

# 5. Close the connection
s.close()

print("Sent data:", MESSAGE)
print("Received data:", data.decode()) # Decode bytes to a string

# WTF? We get http replies? weird.