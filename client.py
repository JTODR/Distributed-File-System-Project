import sys
import client_lib
import os

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
        client_socket = client_lib.create_socket()
        reply_DS = client_lib.look_for_DS(client_socket, filename)
        client_socket.close()

        if reply_DS == "FILE_DOES_NOT_EXIST":
            print(filename + " does not exist on a fileserver")
        else:
            filename_DS = reply_DS.split('|')[0]
            pathname_DS = reply_DS.split('|')[1]
            fileserverIP_DS = reply_DS.split('|')[2]
            fileserverPORT_DS = reply_DS.split('|')[3]

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


        client_socket = client_lib.create_socket()
        file_path = os.path.join(pathname_DS, filename_DS)
        client_lib.send_read_write(client_socket, fileserverIP_DS, int(fileserverPORT_DS), file_path, "a+", write_msg) # send text and filename to the fileserver

        reply = client_socket.recv(1024)
        reply = reply.decode()
        print (reply)
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

        reply = client_socket.recv(1024)    # receive reply from file server
        reply = reply.decode()
        print (reply)

        print("Exiting <read> mode...\n")
        client_socket.close()

        
        
    if "<instructions>" in msg:
        client_lib.instructions()

