import sys
import client_lib
import os
import time
from datetime import datetime

print ("\n")
client_lib.instructions()
client_id = str(datetime.now())

while True:
   
    client_input = sys.stdin.readline()
        
    if "<write>" in client_input:

        # error check the message
        while not client_lib.check_message(client_input):
             client_input = sys.stdin.readline()
        
        filename = client_input.split()[1]

        # ------ INFO FROM DS ------
        client_socket = client_lib.create_socket()  # create socket to directory service
        reply_DS = client_lib.look_for_DS(client_socket, filename)  # request the file info from directory service
        client_socket.close()   # close the connection 

        if reply_DS == "FILE_DOES_NOT_EXIST":
            print(filename + " does not exist on a fileserver")
        else:
            filename_DS = reply_DS.split('|')[0]
            pathname_DS = reply_DS.split('|')[1]
            fileserverIP_DS = reply_DS.split('|')[2]
            fileserverPORT_DS = reply_DS.split('|')[3]

            file_path = os.path.join(pathname_DS, filename_DS)  # attach filename to filepath

            # ------ LOCKING ------
            client_socket = client_lib.create_socket()
            grant_lock = client_lib.lock_unlock_file(client_socket, client_id, file_path, "lock")
            client_socket.close()
            while grant_lock == "file_not_granted":
                print("File not granted, polling again...")
                client_socket = client_lib.create_socket()
                grant_lock = client_lib.lock_unlock_file(client_socket, client_id, file_path, "lock")
                client_socket.close()
                time.sleep(0.5)     # wait 0.5 sec if lock not available and request it again

            print("You are granted the file...")

            # ------ WRITING ------
            print ("Write some text...")
            print ("<end> to finish writing")
            client_lib.print_breaker()
            write_client_input = ""
            while True:
                written = sys.stdin.readline()
                if "<end>" in written:  # check if user wants to finish writing
                    break
                else: 
                    write_client_input += written
            client_lib.print_breaker()

            

            # ------ WRITING TO FS ------
            client_socket = client_lib.create_socket()
            client_lib.send_read_write(client_socket, fileserverIP_DS, int(fileserverPORT_DS), file_path, "a+", write_client_input) # send text and filename to the fileserver
            #print ("SENT FOR WRITE")
            reply_FS = client_socket.recv(1024)
            reply_FS = reply_FS.decode()
            client_socket.close()
            print (reply_FS)

            # ------ UNLOCKING ------
            client_socket = client_lib.create_socket()
            reply_unlock = client_lib.lock_unlock_file(client_socket, client_id, file_path, "unlock")
            client_socket.close()
            print (reply_unlock)



            
        print ("Exiting <write> mode...\n")
        client_socket.close()
        

    if "<read>" in client_input: 
        while not client_lib.check_message(client_input):    # error check the input
             client_input = sys.stdin.readline()

        filename = client_input.split()[1]   # get file name from user

        client_socket = client_lib.create_socket()  # create socket to directory service
        reply_DS = client_lib.look_for_DS(client_socket, filename)  # send file name to directory service
        client_socket.close()   # close directory service connection

        if reply_DS == "FILE_DOES_NOT_EXIST":
            print(filename + " does not exist on a fileserver")
        else:
            # parse info received from the directory service
            filename_DS = reply_DS.split('|')[0]
            pathname_DS = reply_DS.split('|')[1]
            fileserverIP_DS = reply_DS.split('|')[2]
            fileserverPORT_DS = reply_DS.split('|')[3]

            client_socket = client_lib.create_socket()  # create socket to file server
            file_path = os.path.join(pathname_DS, filename_DS)  # join the file to the filepath
            client_lib.send_read_write(client_socket, fileserverIP_DS, int(fileserverPORT_DS), file_path, "r", "READ") # send filepath and read to file server

            reply_FS = client_socket.recv(1024)    # receive reply from file server
            reply_FS = reply_FS.decode()
            print (reply_FS)

        print("Exiting <read> mode...\n")
        client_socket.close()

             
    if "<instructions>" in client_input:
        client_lib.instructions()

    if "<quit>" in client_input:
        print("Exiting application...")
        sys.exit()
