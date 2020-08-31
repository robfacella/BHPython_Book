import socket

target_host = "www.google.com"
target_port = 80

#Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the Client
client.connect((target_host,target_port))

#Send some Data
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

#Receive some Data
response = client.recv(4096)

#Print the Data Received
print (response)
