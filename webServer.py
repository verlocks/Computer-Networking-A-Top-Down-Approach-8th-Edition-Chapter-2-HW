# import socket module
from socket import *
# In order to terminate the program
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
HOST = ""
PORT = 50007
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        print(f'Get message: {message}')
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send one HTTP header line into socket
        responseHeader = "HTTP/1.x 200 OK\n\n"
        connectionSocket.send(responseHeader.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        responseHeader = "HTTP/1.x 404 Not Found\r\n"
        connectionSocket.send(responseHeader.encode())

        # Close client socket
        connectionSocket.close()

serverSocket.close()
# Terminate the program after sending the corresponding data
sys.exit()
