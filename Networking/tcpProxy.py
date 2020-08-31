#!/bin/python
import sys
import socket
import threading

def hexdump(src, length=16):
#This is a hex dump function pulled from <http://code.activatestate.com/recipes/142812-hex-dumper/>
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s =src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append( b"%04X%-*s%s" % (i, length*(digits + 1), hexa, text) )
    print b'\n'.join(result)
def receive_from(connection):
    buffey = ""
    #set a 4 second timeout; depending on target, may need adjustment
    connection.settimeout(4)
    try:
        #keep reading into buffer until end of data or we time out
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffey += data
    except:
        pass
    return buffey
#Modify requests destined for remote host
def request_handler(buffet):
    #perform modifications. is this a joke?
    return buffet
#Modify responses destined for local host
def response_handler(buffet):
    #so it is a joke
    return buffet
##
def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host,local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host,local_port)
        print "[!!] Check for other listening sockets or correct the permissions."
        sys.exit(0)

    print "[*] Listening on %s:%d" % (local_host,local_port)
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        #print local connection info
        print "[==>] Recieved incoming connection from %s:%d" % (addr[0],addr[1])

        #begin thread to communicate with the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket,remote_host,remote_port,receive_first))
        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    #connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))
    #receive data from the remote end if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        #send this to the response handler
        remote_buffer = response_handler(remote_buffer)
        #if we have data to send to our local client, send it
        if len(remote_buffer):
            print "[<==] sending %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)
    #Now loop and read from local; send to remote, to local; rinse, wash and repeat.
    while True:
        #read from local host
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print "[==>] Received %d bytes from localhost." % len(local_buffer)
            hexdump(local_buffer)
            #send to request handler
            local_buffer = request_handler(local_buffer)
            #send off data to remote host
            remote_socket.send(local_buffer)
            print "[==>] sent to remote host."
            #receive a response back in turn
            remote_buffer = receive_from(remote_socket)
            if len(remote_buffer):
                print "[<==] received %d bytes from remote host." % len(remote_buffer)
                hexdump(remote_buffer)
                #response handler
                remote_buffer = response_handler(remote_buffer)
                #send to local socket
                client_socket.send(remote_buffer)
                print "[<==] Sent to localhost."
            #if no more data on either side, close connections
            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                print "[*] No more data. Closing connections."
                break

def main():
    #invalid # of command-line args
    if len(sys.argv[1:]) !=5:
        print "Usage: ./tcpProxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
        print "Example: ./tcpProxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)
    #setup local listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    #setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    #Tells the proxy to connect & receive data before sending to the remote host
    receive_first = sys.argv[5]
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
        #sanitize that NOT True argv
    #create the listening socket
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)
main()
