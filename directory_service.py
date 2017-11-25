# directory service
import os
import csv      #To work with csv file
from socket import *

serverPort = 9090
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')

def check_csv(filename):

	with open("file_mappings.csv",'rt') as infile:        #Unzip the compressed file and open it
		d_reader = csv.DictReader(infile, delimiter=',')    #Read file as a csv file
		header = d_reader.fieldnames    #skip header of csv file
            

		for line in d_reader:
            
			#Use the dictionary reader to read the values of the cells at the current line
			user_filename = line['user_filename']

			if user_filename == filename:
				actual_filename = line['actual_filename']
				file_path = line['path']
				server_addr = line['server_addr']
				server_port = line['server_port']
				print("actual_filename: " + actual_filename)
				print("file_path: " + file_path)
				print("server_addr: " + server_addr)
				print("server_port: " + server_port)
				return actual_filename + "|" + file_path + "|" + server_addr + "|" + server_port 





def main():

	while 1:
		connectionSocket, addr = serverSocket.accept()
		while 1:
			response = ""
			recv_msg = connectionSocket.recv(1024)
			filename = recv_msg.decode()

			#print("RECEIVED: " + filename)

			response = check_csv(filename)

			#print("RESPONSE: " + response)
			connectionSocket.send(response.encode())
			
			#break
		connectionSocket.close()



if __name__ == "__main__":
	main()