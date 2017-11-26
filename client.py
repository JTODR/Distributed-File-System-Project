import sys
import client_lib
import os
import time

print ("\n")
client_lib.instructions()

#client_socket = client_lib.create_socket()

while True:
   
    msg = sys.stdin.readline()
    #client_socket = client_lib.create_socket()
        
    if "<write>" in msg:

        # error check the message
        while not client_lib.check_message(msg):
             msg = sys.stdin.readline()
        
        filename = msg.split()[1]

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

            print ("Write some text...")
            print ("<end> to finish writing")
            client_lib.print_breaker()
            write_msg = ""
            while True:
                written = sys.stdin.readline()
                if "<end>" in written:  # check if user wants to finish writing
                    break
                else: 
                    write_msg += written
            client_lib.print_breaker()

            # ------ LOCKING ------
            client_socket = client_lib.create_socket()
            grant_lock = client_lib.lock_file(client_socket, file_path)

            while grant_lock == "file_not_granted":
                print("Stuck in loop")
                grant_lock = client_lib.lock_file(client_socket, file_path)
                time.sleep.sec(0.5)     # wait 0.5 sec if lock not available and request it again
            client_socket.close()
            print("You are granted the file...")

            # ------ WRITING TO FS ------
            client_socket = client_lib.create_socket()
            client_lib.send_read_write(client_socket, fileserverIP_DS, int(fileserverPORT_DS), file_path, "a+", write_msg) # send text and filename to the fileserver
            reply_FS = client_socket.recv(1024)
            reply_FS = reply_FS.decode()
            client_socket.close()
            print (reply_FS)

            # ------ UNLOCKING ------
            client_socket = client_lib.create_socket()
            reply_unlock = client_lib.unlock_file(client_socket, file_path)
            client_socket.close()
            print (reply_unlock)



            
        print ("Exiting <write> mode...\n")
        client_socket.close()
        

    if "<read>" in msg: 
        while not client_lib.check_message(msg):    # error check the input
             msg = sys.stdin.readline()

        filename = msg.split()[1]   # get file name from user

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

        
        
    if "<instructions>" in msg:
        client_lib.instructions()

