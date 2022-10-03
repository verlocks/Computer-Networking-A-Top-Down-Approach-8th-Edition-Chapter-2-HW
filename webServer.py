from socket import *
import sys
from _thread import *
import threading

print_lock = threading.Lock()


# thread function
def threaded(c):
    try:
        message = c.recv(1024)
        print(f'Get message: {message}')
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send one HTTP header line into socket
        responseHeader = "HTTP/1.x 200 OK\n\n"
        c.send(responseHeader.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            c.send(outputdata[i].encode())
        c.send("\r\n".encode())
        c.close()
        print_lock.release()
        print("Over!")
    except IOError:
        # Send response message for file not found
        responseHeader = "HTTP/1.x 404 Not Found\r\n"
        c.send(responseHeader.encode())

        # Close client socket
        c.close()
        print_lock.release()
        print("Over!")
    except IndexError:
        # Send response message for file not found
        responseHeader = "HTTP/1.x 404 Not Found\r\n"
        c.send(responseHeader.encode())

        # Close client socket
        c.close()
        print_lock.release()
        print("Over!")


serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
HOST = ""
PORT = 50008
serverSocket.bind((HOST, PORT))
serverSocket.listen(10)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    # lock acquired by client
    print_lock.acquire()
    print('Connected to :', addr[0], ':', addr[1])

    # Start a new thread and return its identifier
    start_new_thread(threaded, (connectionSocket,))

serverSocket.close()
# Terminate the program after sending the corresponding data
sys.exit()
