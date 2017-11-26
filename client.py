import sys
import client_lib
import os

print ("\n")
client_lib.instructions()

#client_socket = client_lib.create_socket()
prev_DS = False

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
            #print(filename_DS)
            #print(pathname_DS)
            #print(fileserverIP_DS)
            #print(fileserverPORT_DS)

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
        while not client_lib.check_message(msg):
             msg = sys.stdin.readline()

        filename = msg.split()[1]
        #file = client_lib.open_file(filename, "r")
        client_lib.send_read_write(client_socket, filename, "r", "READ")
        reply = client_socket.recv(1024)
        reply = reply.decode()
        print (reply)
        #if file != IOError:
        #    print (file.read())
        
        
    if "<instructions>" in msg:
        client_lib.instructions()


    #if "<lookfor>" in msg:
     #   if prev_DS == False:
     #       serverName = 'localhost'
     #       serverPort = 9090
     #       client_socket.connect((serverName,serverPort))

     #   filename = msg.split()[1]

      #  reply_DS = client_lib.send_DS(client_socket, filename)
        #print (reply_DS)
      #  if reply_DS == "FILE_DOES_NOT_EXIST":
       #     print(filename + " does not exist on a fileserver")
      #  else:
      #      filename_DS = reply_DS.split('|')[0]
      #      pathname_DS = reply_DS.split('|')[1]
      #      fileserverIP_DS = reply_DS.split('|')[2]
      #      fileserverPORT_DS = reply_DS.split('|')[3]
       #     print(filename_DS)
       #     print(pathname_DS)
       #     print(fileserverIP_DS)
        #    print(fileserverPORT_DS)
#
       # prev_DS = True
        #client_socket.close()
        