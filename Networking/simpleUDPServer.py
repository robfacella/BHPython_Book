import socket

#local host
target_host = "127.0.0.1"
#Create a Socket Object
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Port to Listen on
UDP_Port = 1123
#Size of Listening Buffer
Buffer_Size = 1024
#Begin listening
server.bind((target_host, UDP_Port))
#Loop Forever
while True:
	#Receive data
	data, addr = server.recvfrom(Buffer_Size)
	#Print that Information
	print data, addr
