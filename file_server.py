# file server
from socket import *

serverAddr = "localhost"
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverAddr, serverPort))
serverSocket.listen(10)
print ('FILE SERVER is ready to receive')

def read_write(filepath, RW, text):
    
    if RW == "r":
        # check if file to read from exists in the directory
        try:
            file = open(filepath, RW)
            text_in_file = file.read()
            return text_in_file
        except IOError:
            print (filepath + " does not exist in directory\n")
            return IOError
            pass
  
    elif RW == "a+":
        file = open(filepath, RW)
        file.write(text)
        return "Success"
    




while 1:
	#connectionSocket, addr = serverSocket.accept()
	while 1:
		response = ""
		connectionSocket, addr = serverSocket.accept()

		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()

		if recv_msg != "":
			filepath = recv_msg.split("|")[0]
			print ("Filepath: " + filepath)
			RW = recv_msg.split("|")[1]
			print ("RW: " + RW)
			text = recv_msg.split("|")[2]
			print ("TEXT: " + text)

			response = read_write(filepath, RW, text)

			if response == "Success":
				reply = "File successfully written to..."
				connectionSocket.send(reply.encode())
				#print ("Sent: " + reply)

			elif response is not IOError and RW == "r":
				reply = "------------------------\n" \
				+ response \
				+ "------------------------" 
				connectionSocket.send(reply.encode())
				#print ("Sent: " + reply)

			elif response is IOError: 
				reply = "File does not exist\n"
				connectionSocket.send(reply.encode())
				#print ("Sent: " + reply)

		
		#break
	connectionSocket.close()