# directory service
import os
import csv      #To work with csv file
from socket import *

serverPort = 9090
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(10)
print ('DIRECTORY SERVICE is ready to receive...')

def check_mappings(filename, list_files):

	with open("file_mappings.csv",'rt') as infile:        # open the .csv file storing the mappings
		d_reader = csv.DictReader(infile, delimiter=',')    # read file as a csv file, taking values after commas
		header = d_reader.fieldnames    	# skip header of csv file
		file_row = ""
		for row in d_reader:
			if list_files == False:
				# use the dictionary reader to read the values of the cells at the current row
				user_filename = row['user_filename']

				if user_filename == filename:		# check if file inputted by the user exists	(eg. file123)
					actual_filename = row['actual_filename']	# get actual filename (eg. file123.txt)
					file_path = row['path']						# get the path to this file
					server_addr = row['server_addr']			# get the file's file server IP address
					server_port = row['server_port']			# get the file's file server PORT number

					print("actual_filename: " + actual_filename)
					print("file_path: " + file_path)
					print("server_addr: " + server_addr)
					print("server_port: " + server_port)

					return actual_filename + "|" + file_path + "|" + server_addr + "|" + server_port	# return string with the information on the file
			else:
				user_filename = row['user_filename']
				file_row = file_row + user_filename +  "\n"

	return file_row		# if file does not exist return None


def main():

	while 1:
		connectionSocket, addr = serverSocket.accept()

		response = ""
		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()

		#print("RECEIVED: " + filename)

		if "LIST" not in recv_msg:
			response = check_mappings(recv_msg, False)		# check the mappings for the file
		elif "LIST" in recv_msg:
			response = check_mappings(recv_msg, True)

		if response is not None:	# for existance of file
			response = str(response)
			print("RESPONSE: \n" + response)
			print("\n")
		else:
			response = "FILE_DOES_NOT_EXIST"

		connectionSocket.send(response.encode())	# send the file information or non-existance message to the client
			
		connectionSocket.close()


if __name__ == "__main__":
	main()