from socket import *
import sys

serverAddr = "localhost"
serverPort = 4040
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverAddr, serverPort))
serverSocket.listen(10)
print ('LOCKING SERVICE is ready to receive')



def check_if_unlocked(file_path, filepath_locked_map):
# NEED TO ADD ALL FILES TO DICTIONARY FIRST!!! or something like that
	
	
	if file_path in filepath_locked_map:		# check for existance of filepath as a key in the dictionary
		if filepath_locked_map[file_path] == "unlocked":
			return True
		else:
			return False
	else:
		filepath_locked_map[file_path] = "unlocked"
		return True





def main():

	filepath_locked_map = {}


	while 1:
		connectionSocket, addr = serverSocket.accept()
		response = ""
		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()

		print("\n" + recv_msg)

		if "_1_:" in recv_msg:
			file_path = recv_msg.split("_1_:")[1]
			
			unlocked = check_if_unlocked(file_path, filepath_locked_map)
			if unlocked == True:
				filepath_locked_map[file_path] = "locked"
				response = "file_granted"
				print("SENT: " + response)
				connectionSocket.send(response.encode())
			else:
				response = "file_not_granted"
				print("SENT: " + response)
				connectionSocket.send(response.encode())

		elif "_2_:" in recv_msg:
			file_path = recv_msg.split("_2_:")[1]
			#file_path.replace(" ", "")	# remove any spaces in the filepath, to use as dict key
			filepath_locked_map[file_path] = "unlocked"
			response = "File unlocked..."
			connectionSocket.send(response.encode())





		connectionSocket.close()



if __name__ == "__main__":
	main()