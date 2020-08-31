import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Listen on Designated port
server.bind((bind_ip,bind_port))
#Max connection Backlog
server.listen(5)

#print some feedback
print "[*] Listening on %s:%d" % (bind_ip,bind_port)

# Client Handling Thread
def handleClient(clientSocket):
	#Recieve Data & Print what the Client Sent
	request = clientSocket.recv(1024)
	print "[*] Received: %s" %request

	#respond with a packet
	clientSocket.send("ACK!")
	#Close Connection
	clientSocket.close
#Main Loop
while True:
	client,addr = server.accept()
	print "[*] Accepted connection from: %s:%d" % (addr[0],addr[1])
	#create client thread to handle incoming data
	clientHandler = threading.Thread(target=handleClient,args=(client,))
	clientHandler.start()
