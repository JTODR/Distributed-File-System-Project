# file server
from socket import *

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')

def read_write(filename, RW, text):
    
    if RW == "r":
        # check if file to read from exists in the directory
        try:
            file = open(filename, RW)
            return True
        except IOError:
            print (filename + " does not exist in directory")
            return False
            pass
  
    elif RW == "a+":
        file = open(filename, RW)
        file.write(text)
        #print (filename + " is open for writing")
        return True
    




while 1:
	connectionSocket, addr = serverSocket.accept()
	while 1:
		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()

		filename = recv_msg.split("\n")[1]
		print ("Filename: " + filename)
		RW = recv_msg.split("\n")[3]
		print ("RW: " + RW)
		text = recv_msg.split("TEXT:")[1]
		print ("TEXT: " + text)


		response = read_write(filename, RW, text)
		if response == True:# and (RW == "a+"):
			reply = filename + " successfully written to"
			connectionSocket.send(reply.encode())
			print ("Sent: " + reply)

		
		#break
	connectionSocket.close()

