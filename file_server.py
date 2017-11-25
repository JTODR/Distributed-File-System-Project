# file server
from socket import *

serverAddr = "95.44.197.33"
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverAddr, serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')

def read_write(filename, RW, text):
    
    if RW == "r":
        # check if file to read from exists in the directory
        try:
            file = open(filename, RW)
            text_in_file = file.read()
            return text_in_file
        except IOError:
            print (filename + " does not exist in directory\n")
            return IOError
            pass
  
    elif RW == "a+":
        file = open(filename, RW)
        file.write(text)
        return "Success"
    




while 1:
	connectionSocket, addr = serverSocket.accept()
	while 1:
		response = ""
		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()

		filename = recv_msg.split("\n")[1]

		print ("Filename: " + filename)
		RW = recv_msg.split("\n")[3]
		print ("RW: " + RW)
		text = recv_msg.split("TEXT:")[1]
		print ("TEXT: " + text)

		response = read_write(filename, RW, text)

		if response == "Success":
			reply = filename + " successfully written to"
			connectionSocket.send(reply.encode())
			#print ("Sent: " + reply)

		elif response is not IOError and RW == "r":
			reply = "------ " + filename + " ------\n" \
			+ response \
			+ "------------------------\n" 
			connectionSocket.send(reply.encode())
			#print ("Sent: " + reply)

		elif response is IOError: 
			reply = filename +  " does not exist\n"
			connectionSocket.send(reply.encode())
			#print ("Sent: " + reply)

		
		#break
	connectionSocket.close()

