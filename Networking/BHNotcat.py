#!/bin/python
import sys
import socket
import getopt
import threading
import subprocess
#BHPython's NO netcat workaround
#Defining some Global Vars
listen		= False
command		= False
upload		= False
execute		= ""
target		= ""
upload_Dest	= ""
port		= 0

def usage():
	print "BHPython NetTool"
	print " "
	print "Usage: BHNotcat.py -t target_host -p port"
	print "-l --listen		-listen on [host]:[port] for incoming connections"
	print "-e --execute=fileToRun   -execute the given file upon receiving a connection"
	print "-c --command		-initialize a command shell"
	print "-u --upload=destination  -upon receiving connection upload a file and write to [destination]"
	print " "
	print " "
	print "Examples: "
	print "BHNotcat.py -t 192.168.0.1 -p 5555 -l -c"
	print "BHNotcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
	print "BHNotcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
	print "echo 'ABCDEFGHI' | ./BHNotcat.py -t 192.168.11.12 -p 135"
	sys.exit(0)
def main():
	global listen
	global port
	global execute
	global command
	global upload_Dest
	global target
	#Not using upload bool yet.
	#No args? display usage()
	if not len(sys.argv[1:]):
		usage()
	#Try reading cli options
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:", ["help","listen","execute","target","port","command","upload"])
	except getopt.GetoptError as err:
		print str(err)
		usage()
	for o,a in opts:
		if o in ("-h","--help"):
			usage()
		elif o in ("-l","--listen"):
			listen = True
		elif o in ("-e", "--execute"):
			execute = a
		elif o in ("-c", "--commandshell"):
			command = True
		elif o in ("-u", "--upload"):
			upload_Dest = a
		elif o in ("-t", "--target"):
			target = a
		elif o in ("-p", "--port"):
			port = int(a)
		else:
			assert False,"Unhandled Option"
	#Listen? Or send data from stdin?
	if not listen and len(target) and port > 0:
		#read in the buffer from the commandline
		#this will block, so send CTRL-D if not sending input to stdin
		buffer = sys.stdin.read()
		#send data off
		client_sender(buffer)
	#will listen and potentially upload things, exec commands,
	#drop a shell back. Depending on command line options above
	if listen:
		server_loop()
main()
