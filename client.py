import sys
import client_lib

print ("\n")
client_lib.instructions()

print ("<instructions> - lets you see the instructions again\n")

while True:
   
    msg = sys.stdin.readline()
        
        
    if "<write>" in msg:

        while not client_lib.check_message(msg):
             msg = sys.stdin.readline()
        

        new_file = False
        filename = msg.split()[1]
        file = client_lib.open_file(filename, "a+")

        print ("Write some text to the file...")
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

        file.write(write_msg)

        print ("Text is saved to " + filename)
        print ("Exiting <write> mode...\n")
        
        
    if "<read>" in msg: 
        filename = msg.split()[1]
        file = client_lib.open_file(filename, "r")
        if file != IOError:
            print (file.read())
        
        
    if "<instructions>" in msg:
        client_lib.instructions()

    else:
        client_lib.instructions()        

