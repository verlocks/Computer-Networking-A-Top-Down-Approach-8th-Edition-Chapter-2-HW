import socket
import sys
from _thread import *
import threading

print_lock = threading.Lock()

SERVER = sys.argv[1]
PORT = int(sys.argv[2])
filename = sys.argv[3]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

message = "GET /" + filename + " HTTP/1.1\r\n\r\n"
client.send(message.encode())

while True:
    in_data = client.recv(1024)
    if not in_data:
        print("Not receive data, end connect.")
        break
    print("From Server :", in_data.decode())

client.close()
