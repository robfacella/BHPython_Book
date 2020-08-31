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
usage()
