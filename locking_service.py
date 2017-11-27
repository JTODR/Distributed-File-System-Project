from socket import *
from collections import defaultdict		# for dictionary list 
import sys

serverAddr = "localhost"
serverPort = 4040
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverAddr, serverPort))
serverSocket.listen(10)
print ('LOCKING SERVICE is ready to receive...')

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
		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()

		print("\nRECEIVED: " + recv_msg )

		if "_1_:" in recv_msg:
			client_id = recv_msg.split("_1_:")[0]
			file_path = recv_msg.split("_1_:")[1]
			waiting_client = False

			unlocked = check_if_unlocked(file_path, filepath_locked_map)
			if unlocked == True:
				count_temp = 0		# a count to check if current client is first in the queue

				if len(filepath_clients_map[file_path]) == 0:	# if no clients currently waiting on the file
					filepath_locked_map[file_path] = "locked"	# lock the file
					grant_message = "file_granted"
					print("SENT: " + grant_message + " ---- " + client_id)
					connectionSocket.send(grant_message.encode())	# send the grant message

				elif file_path in filepath_clients_map:			
					for file_path,values in filepath_clients_map.items():	# find the current file path in the map
						for v in values:									# iterate though the clients waiting on this file path
							if v == client_id and count_temp == 0:			# if the client is the first client waiting
								filepath_clients_map[file_path].remove(v)	# remove it from the waiting list
								filepath_locked_map[file_path] = "locked"	# lock the file
								grant_message = "file_granted"			
								print("SENT: " + grant_message +" ---- " + client_id)	
								connectionSocket.send(grant_message.encode())	# send the grant message
							count_temp += 1

			else:				# if the file is locked
				grant_message = "file_not_granted"

				if file_path in filepath_clients_map:						
					for file_path,values in filepath_clients_map.items():	# find the current file path in the map
						for v in values:							# iterate though the clients waiting on this file path
							if v == client_id:					# check if client is already waiting on the file
								waiting_client = True			# if already waiting, set flag - so client is not added to waiting list multiple times for the file path
				
				if waiting_client == False:			# if not already waiting
					filepath_clients_map[file_path].append(client_id)	# append client to lists of clients waiting for the file

				print("SENT: " + grant_message + client_id)
				connectionSocket.send(grant_message.encode())	# send file not granted message

		elif "_2_:" in recv_msg:		# if unlock message (_2_) received 
			client_id = recv_msg.split("_2_:")[0]
			file_path = recv_msg.split("_2_:")[1]

			filepath_locked_map[file_path] = "unlocked"		# unlock the current file
			grant_message = "File unlocked..."
			connectionSocket.send(grant_message.encode())	# tell the current client that the file was unlocked

		connectionSocket.close()



if __name__ == "__main__":
	main()