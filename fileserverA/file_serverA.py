# file server
from socket import *

server_addr = "localhost"
server_port = 12001
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind((server_addr, server_port))
server_socket.listen(10)
print ('FILE SERVER is ready to receive...')

file_version_map = {}


def replicate(filename):

	f = open(filename, 'r')
	text = f.read()
	f.close()

	msg = "REPLICATE|" + filename + "|" + text + "|" + str(file_version_map[filename])

	port = 12002
	server_ip = 'localhost'
	print("Replicating to fileserver B")
	replicate_socket = socket(AF_INET, SOCK_STREAM)
	replicate_socket.connect((server_ip,port))
	replicate_socket.send(msg.encode())
	replicate_socket.close()

	port = 12003
	server_ip = 'localhost'
	print("Replicating to fileserver C")
	replicate_socket = socket(AF_INET, SOCK_STREAM)
	replicate_socket.connect((server_ip,port))
	replicate_socket.send(msg.encode())
	replicate_socket.close()



def read_write(filename, RW, text, file_version_map):
	if RW == "r":	# if read request
		try:
			file = open(filename, RW)	
			text_in_file = file.read()		# read the file's text into a string
			if filename not in file_version_map:
				file_version_map[filename] = 0
			return (text_in_file, file_version_map[filename])			
		except IOError:				# IOError occurs when open(filepath,RW) cannot find the file requested
			print (filename + " does not exist in directory\n")
			return (IOError, -1)
			pass

	elif RW == "a+":	# if write request

		if filename not in file_version_map:
			file_version_map[filename] = 0		# if empty (ie. if its a new file), set the version no. to 0
		else:
			file_version_map[filename] = file_version_map[filename] + 1		# increment version no.
			print("Updated " + filename + " to version " + str(file_version_map[filename]))

		file = open(filename, RW)
		file.write(text)

		
		print("FILE_VERSION: " + str(file_version_map[filename]))
		return ("Success", file_version_map[filename])


def send_client_reply(response, RW, connection_socket):

	if response[0] == "Success":
		reply = "File successfully written to..." + str(response[1])

		print("Sending file version " + str(response[1]))
		connection_socket.send(reply.encode())
		#print ("Sent: " + reply)

	elif response[0] is not IOError and RW == "r":
		connection_socket.send(response.encode())
		#print ("Sent: " + reply)

	elif response[0] is IOError: 
		reply = "File does not exist\n"
		connection_socket.send(reply.encode())
		#print ("Sent: " + reply)
	
def main():

	

	while 1:
		response = ""
		connection_socket, addr = server_socket.accept()

		recv_msg = connection_socket.recv(1024)
		recv_msg = recv_msg.decode()

		#print("RECEIVED: " + recv_msg)

		if recv_msg != "" and "CHECK_VERSION" not in recv_msg:
			# parse the message

			filename = recv_msg.split("|")[0]	# file path to perform read/write on
			print ("Filename: " + filename)
			RW = recv_msg.split("|")[1]			# whether its a read or write
			print ("RW: " + RW)
			text = recv_msg.split("|")[2]		# the text to be written (this text is "READ" for a read and is ignored)
			print ("TEXT: " + text)

			response = read_write(filename, RW, text, file_version_map)	# perform the read/write and check if successful
			send_client_reply(response, RW, connection_socket)		# send back write successful message or send back text for client to read

			if RW == 'a+':
				replicate(filename)


		elif "CHECK_VERSION" in recv_msg:
			client_filename = recv_msg.split("|")[1]			# parse the version number to check
			print("Version check on " + client_filename)
			file_version = str(file_version_map[client_filename])
			connection_socket.send(file_version.encode())


	connection_socket.close()

if __name__ == "__main__":
	main()