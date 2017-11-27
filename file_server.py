# file server
from socket import *

server_addr = "localhost"
server_port = 12000
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind((server_addr, server_port))
server_socket.listen(10)
print ('FILE SERVER is ready to receive...')

def read_write(filepath, RW, text):
    
    if RW == "r":	# if read request
        # check if file to read from exists in the directory
        try:
            file = open(filepath, RW)	
            text_in_file = file.read()		# read the file's text into a string
            return text_in_file			
        except IOError:				# IOError occurs when open(filepath,RW) cannot find the file requested
            print (filepath + " does not exist in directory\n")
            return IOError
            pass
  
    elif RW == "a+":	# if write request
        file = open(filepath, RW)
        file.write(text)	# write the text from the client to the file
        return "Success"


def send_client_reply(response, RW, connection_socket):

	if response == "Success":
		reply = "File successfully written to..."
		connection_socket.send(reply.encode())
		#print ("Sent: " + reply)

	elif response is not IOError and RW == "r":
		reply = "------------------------\n" \
		+ response \
		+ "------------------------" 
		connection_socket.send(reply.encode())
		#print ("Sent: " + reply)

	elif response is IOError: 
		reply = "File does not exist\n"
		connection_socket.send(reply.encode())
		#print ("Sent: " + reply)
    
def main():

	while 1:
		response = ""
		connection_socket, addr = server_socket.accept()

		recv_msg = connection_socket.recv(1024)
		recv_msg = recv_msg.decode()

		if recv_msg != "":
			# parse the message
			filepath = recv_msg.split("|")[0]	# file path to perform read/write on
			print ("Filepath: " + filepath)
			RW = recv_msg.split("|")[1]			# whether its a read or write
			print ("RW: " + RW)
			text = recv_msg.split("|")[2]		# the text to be written (this text is "READ" for a read and is ignored)
			print ("TEXT: " + text)

			response = read_write(filepath, RW, text)	# perform the read/write and check if successful
			send_client_reply(response, RW, connection_socket)		# send back write successful message or send back text for client to read

	connection_socket.close()

if __name__ == "__main__":
	main()