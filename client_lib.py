from socket import *
import sys

def create_socket():
    # create client socket and return socket object
    #serverName = 'address'
    #serverPort = 9090
    s = socket(AF_INET, SOCK_STREAM)
    #s.connect((address,port))
    return s

def send_read_write(client_socket, fileserverIP_DS, fileserverPORT_DS, file_path , RW, msg):

    # set up string to send
    #send_msg = "FILEPATH: \n" + file_path + "\n" \
    #+ "READWRITE: \n" + RW + "\n" \
    #+ "TEXT:" + msg
    send_msg = file_path + "|" + RW + "|" + msg

    # send the sting requesting a write to the file server
    client_socket.connect((fileserverIP_DS,fileserverPORT_DS))
    client_socket.send(send_msg.encode())

def look_for_DS(client_socket, filename):
    serverName = 'localhost'
    serverPort = 9090
    client_socket.connect((serverName,serverPort))

    # send the sting requesting a write to the file server
    client_socket.send(filename.encode())
    reply = client_socket.recv(1024)
    reply = reply.decode()
    #client_socket.close()
    #print (reply)
    return reply


def instructions():
    # instructions to the user
    print ("------------------- INSTRUCTIONS ----------------------")
    print ("<lookfor> - to look for location of a file")
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