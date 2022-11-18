# UDPPingerClient.py
from socket import *
import datetime

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.settimeout(1)

# Assign IP address and port number to socket
serverSocket.bind(('', 12001))
print("Please enter the target address and port number.")
print("IP address:")
address = input()
print("port number:")
port = int(input())

minRTT = 1001
maxRTT = -1
sumRTT = 0
lossPack = 0
for i in range(10):
    sendTime = datetime.datetime.now()
    sendMessage = str.encode('Ping ' + str(i+1) + ' ' + str(sendTime))
    serverSocket.sendto(sendMessage, (address, port))
    # Receive the client packet along with the address it is coming from
    try:
        recvMessage, recvAddress = serverSocket.recvfrom(1024)
        while recvMessage != sendMessage.upper() and recvAddress != (address, port):
            recvMessage, address = serverSocket.recvfrom(1024)
        recvTime = datetime.datetime.now()
        print(recvMessage)
        duration = recvTime - sendTime
        minRTT = min(minRTT, duration.microseconds)
        maxRTT = max(maxRTT, duration.microseconds)
        sumRTT += duration.microseconds
        print(f"PING {i+1}/10 RTT: {duration.microseconds} ms")
    except TimeoutError:
        lossPack += 1
        print(f"PING {i+1}/10 Request timed out")
print(f"minRTT: {minRTT} ms | maxRTT: {maxRTT} ms | \
avgRTT: {round(sumRTT/(10-lossPack), 2)} ms | lossRate: {lossPack*10}%")