import sys
import client_lib

print ("\n")
client_lib.instructions()

client_socket = client_lib.create_socket()

while True:
   
    msg = sys.stdin.readline()
        
        
    if "<write>" in msg:

        # error check the message
        while not client_lib.check_message(msg):
             msg = sys.stdin.readline()
        
        filename = msg.split()[1]

        print ("Write some text...")
        print ("<end> to finish writing")
        client_lib.print_breaker()

        write_msg = ""

        while True:
            written = sys.stdin.readline()
            if "<end>" in written:
                break
            else: 
                write_msg += written

        client_lib.print_breaker()

        client_lib.send_write(client_socket, filename, "a+", write_msg)

        #client_socket = client_lib.create_socket()
        reply = client_socket.recv(1024)
        reply = reply.decode()
        print ("SERVER: " + reply)
        #client_socket.close()

        print ("Text is saved to " + filename)
        print ("Exiting <write> mode...\n")
        
        
    if "<read>" in msg: 
        while not client_lib.check_message(msg):
             msg = sys.stdin.readline()

        filename = msg.split()[1]
        file = client_lib.open_file(filename, "r")
        if file != IOError:
            print (file.read())
        
        
    if "<instructions>" in msg:
        client_lib.instructions()

    else:
        if len(msg) > 1:
            client_lib.instructions()     

