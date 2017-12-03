import sys
import client_lib
from datetime import datetime
from time import gmtime, strftime

def main():

    print ("\n")
    client_lib.instructions()
    client_id = strftime("%Y%m%d%H%M%S", gmtime())
    file_version_map = {}

    while True:
       
        client_input = sys.stdin.readline()
            
        if "<write>" in client_input:
            while not client_lib.check_valid_input(client_input):       # error check the input
                 client_input = sys.stdin.readline()
            
            filename = client_input.split()[1]      # get the filename from the input
            response = client_lib.handle_write(filename, client_id, file_version_map)    # handle the write request
            if response == False:
                print("File unlock polling timeout...")
                print("Try again later...")
            print ("Exiting <write> mode...\n")
            

        if "<read>" in client_input:
            while not client_lib.check_valid_input(client_input):    # error check the input
                 client_input = sys.stdin.readline()

            filename = client_input.split()[1]   # get file name from the input
            client_lib.handle_read(filename, file_version_map, client_id)        # handle the read request 
            print("Exiting <read> mode...\n")
        
        if "<list>" in client_input:
            client_socket = client_lib.create_socket()
            client_lib.send_directory_service(client_socket, "", True)
            client_socket.close()

        #if "<create>" in client_input:
        #    while not client_lib.check_valid_input(client_input):       # error check the input
        #         client_input = sys.stdin.readline()
        #    filename = client_input.split()[1]
        #    client_lib.create_file(filename)

        if "<instructions>" in client_input:
            client_lib.instructions()


        if "<quit>" in client_input:
            print("Exiting application...")
            sys.exit()

if __name__ == "__main__":
    main()