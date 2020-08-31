import socket

target_host = "127.0.0.1"
target_port = 9999

#Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the Client
client.connect((target_host,target_port))

#Send some Data
client.send("Hello")

#Receive some Data
response = client.recv(4096)

#Print the Data Received
print (response)
