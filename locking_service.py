from socket import *
from collections import defaultdict		# for dictionary list 
import sys

serverAddr = "localhost"
serverPort = 4040
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverAddr, serverPort))
serverSocket.listen(10)
print ('LOCKING SERVICE is ready to receive...')

def check_if_unlocked(filename, filename_locked_map):

	
	if filename in filename_locked_map:		# check for existance of filename as a key in the dictionary
		if filename_locked_map[filename] == "unlocked":
			return True
		else:
			return False
	else:
		filename_locked_map[filename] = "unlocked"
		return True

def main():

	filename_locked_map = {}
	filename_clients_map = defaultdict(list)
	waiting_client = False
	client_timeout_map = {}


	while 1:
		connectionSocket, addr = serverSocket.accept()
		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()

		print("\nRECEIVED: " + recv_msg )

		if "_1_:" in recv_msg:
			client_id = recv_msg.split("_1_:")[0]
			filename = recv_msg.split("_1_:")[1]
			waiting_client = False


			unlocked = check_if_unlocked(filename, filename_locked_map)
			if unlocked == True:
				count_temp = 0		# a count to check if current client is first in the queue

				if len(filename_clients_map[filename]) == 0:	# if no clients currently waiting on the file
					filename_locked_map[filename] = "locked"	# lock the file
					grant_message = "file_granted"
					print("SENT: " + grant_message + " ---- " + client_id)
					connectionSocket.send(grant_message.encode())	# send the grant message

				elif filename in filename_clients_map:			
					for filename,values in filename_clients_map.items():	# find the current file in the map
						for v in values:									# iterate though the clients waiting on this file
							if v == client_id and count_temp == 0:			# if the client is the first client waiting
								filename_clients_map[filename].remove(v)	# remove it from the waiting list
								filename_locked_map[filename] = "locked"	# lock the file
								grant_message = "file_granted"			
								print("SENT: " + grant_message +" ---- " + client_id)	
								connectionSocket.send(grant_message.encode())	# send the grant message
							count_temp += 1

			else:				# if the file is locked
				grant_message = "file_not_granted"

				if client_id in client_timeout_map:		# check if first time requesting file
					client_timeout_map[client_id] = client_timeout_map[client_id] + 1		# if first time, set timeout value to 0
					print("TIME: " + str(client_timeout_map[client_id]))
				else:
					client_timeout_map[client_id] = 0	# if not first time, increment timeout value of client


				if client_timeout_map[client_id] == 100:	# if client polled 100 times (10 sec), send timeout
					timeout_msg = "TIMEOUT"
					for filename,values in filename_clients_map.items():	# find the current file in the map
						for v in values:									# iterate though the clients waiting on this file 
							if v == client_id:		# if the client is the first client waiting
								filename_clients_map[filename].remove(v)	# remove it from the waiting list
					del client_timeout_map[client_id]			# remove client from timeout map
					connectionSocket.send(timeout_msg.encode())	# send timeout msg
				else:

					if filename in filename_clients_map:						
						for filename,values in filename_clients_map.items():	# find the current file in the map
							for v in values:							# iterate though the clients waiting on this file 
								if v == client_id:					# check if client is already waiting on the file
									waiting_client = True			# if already waiting, set flag - so client is not added to waiting list multiple times for the file 
					
					if waiting_client == False:			# if not already waiting
						filename_clients_map[filename].append(client_id)	# append client to lists of clients waiting for the file

					print("SENT: " + grant_message + client_id)
					connectionSocket.send(grant_message.encode())	# send file not granted message

		elif "_2_:" in recv_msg:		# if unlock message (_2_) received 
			client_id = recv_msg.split("_2_:")[0]
			filename = recv_msg.split("_2_:")[1]

			filename_locked_map[filename] = "unlocked"		# unlock the current file
			grant_message = "File unlocked..."
			connectionSocket.send(grant_message.encode())	# tell the current client that the file was unlocked

		connectionSocket.close()



if __name__ == "__main__":
	main()