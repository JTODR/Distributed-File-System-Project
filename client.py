import sys
import client_lib
from datetime import datetime
from time import gmtime, strftime

def main():

    print ("\n")
    client_lib.instructions()
    client_id = strftime("%Y%m%d%H%M%S", gmtime())
    #client_id = str(datetime.now())     # assign a client id, this will be used to in the locking service
    file_version_map = {}

    while True:
       
        client_input = sys.stdin.readline()
            
        if "<write>" in client_input:
            while not client_lib.check_valid_input(client_input):       # error check the input
                 client_input = sys.stdin.readline()
            
            filename = client_input.split()[1]      # get the filename from the input
            client_lib.handle_write(filename, client_id, file_version_map)    # handle the write request
            print ("Exiting <write> mode...\n")
            

        if "<read>" in client_input:
            while not client_lib.check_valid_input(client_input):    # error check the input
                 client_input = sys.stdin.readline()

            filename = client_input.split()[1]   # get file name from the input
            client_lib.handle_read(filename, file_version_map, client_id)        # handle the read request 
            print("Exiting <read> mode...\n")
            

        if "<instructions>" in client_input:
            client_lib.instructions()


        if "<quit>" in client_input:
            print("Exiting application...")
            sys.exit()

if __name__ == "__main__":
    main()