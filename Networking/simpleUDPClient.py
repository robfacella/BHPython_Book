import socket
#create client
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Set a IP & Port to SendTo
UDP_IP = '127.0.0.1'
UDP_Port = 1123
#Some BS Data to send
count = 0
while True:
	#Create Message to Send
	MESSAGE = str(count)
	#Create Entrophy with the BS Data
	count +=1
	#Send Message
	sock.sendto(MESSAGE, (UDP_IP, UDP_Port))
