from socket import *
import sys

def create_socket():
    # create client socket and return socket object
    serverName = 'localhost'
    serverPort = 9090
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((serverName,serverPort))
    return s

def send_read_write(client_socket, filename, RW, msg):

    # set up string to send
    send_msg = "FILENAME: \n" + filename + "\n" \
    + "READWRITE: \n" + RW + "\n" \
    + "TEXT:" + msg

    # send the sting requesting a write to the file server
    client_socket.send(send_msg.encode())

def send_DS(client_socket, filename):

    # send the sting requesting a write to the file server
    client_socket.send(filename.encode())



def instructions():
    # instructions to the user
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