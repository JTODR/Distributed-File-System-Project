from socket import *
from collections import defaultdict		# for dictionary list 
from collections import deque
import sys

#client_id = 0 	# assign ids to clients when they request a locked file

serverAddr = "localhost"
serverPort = 4040
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverAddr, serverPort))
serverSocket.listen(10)
print ('LOCKING SERVICE is ready to receive')



def check_if_unlocked(file_path, filepath_locked_map):

	
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
	filepath_clients_map = defaultdict(list)
	waiting_client = False


	while 1:
		connectionSocket, addr = serverSocket.accept()
		response = ""
		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()

		#print("\n" + recv_msg)

		if "_1_:" in recv_msg:
			waiting_client = False
			client_id = recv_msg.split("_1_:")[0]
			file_path = recv_msg.split("_1_:")[1]
			
			unlocked = check_if_unlocked(file_path, filepath_locked_map)
			if unlocked == True:
				filepath_locked_map[file_path] = "locked"
				response = "file_granted"
				print("SENT: " + response)
				connectionSocket.send(response.encode())
			else:
				response = "file_not_granted"

				
				print("--- Wait dict ---")
				if file_path in filepath_clients_map:			
					for file_path,values in filepath_clients_map.items():
						for v in values:
							if v == client_id:
								waiting_client = True
								
							print(file_path," : ",v)
							#if waiting_client == False:
							#	filepath_clients_map[file_path].append(client_id)	# append client to lists of clients waiting for the file
					
				print("------------------")			
				
				if waiting_client == False:
					filepath_clients_map[file_path].append(client_id)	# append client to lists of clients waiting for the file


				print("SENT: " + response)
				connectionSocket.send(response.encode())

		elif "_2_:" in recv_msg:
			client_id = recv_msg.split("_2_:")[0]
			file_path = recv_msg.split("_2_:")[1]

			filepath_locked_map[file_path] = "unlocked"
			response = "File unlocked..."
			connectionSocket.send(response.encode())





		connectionSocket.close()



if __name__ == "__main__":
	main()