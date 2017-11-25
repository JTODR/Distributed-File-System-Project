from socket import *
import sys




def create_socket():
    serverName = 'localhost'
    serverPort = 12000
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((serverName,serverPort))
    return s

def send_write(client_socket, filename, RW, msg):

    send_msg = "FILENAME: \n" + filename + "\n" \
    + "READWRITE: \n" + RW + "\n" \
    + "TEXT:" + msg + "\n"
    
    client_socket.send(send_msg.encode())
    #client_socket.close()
    #print ("MESSAGE SENT!")
    


def instructions():
    print ("------------------- INSTRUCTIONS ----------------------")
    print ("<write> [filename] - write to file mode")
    print ("<end> - finish writing")
    print ("<read> [filename] - read a file in your current directory")
    print ("<instructions> - lets you see the instructions again")
    print ("-------------------------------------------------------\n")

def print_breaker():
    print ("--------------------------------")

def check_message(msg):
    # check for correct format for message split
    if len(msg.split()) < 2:
        print ("Incorrect format")
        instructions()
        return False
    else:
        return True