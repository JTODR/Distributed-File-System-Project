from socket import *
import sys

def create_socket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

def send_read_write(client_socket, fileserverIP_DS, fileserverPORT_DS, file_path , RW, msg):

    send_msg = file_path + "|" + RW + "|" + msg

    # send the sting requesting a write to the file server
    client_socket.connect((fileserverIP_DS,fileserverPORT_DS))
    client_socket.send(send_msg.encode())

def look_for_DS(client_socket, filename):
    serverName = 'localhost'
    serverPort = 9090   # port of directory service
    client_socket.connect((serverName,serverPort))

    # send the string requesting file info to directory service
    client_socket.send(filename.encode())
    reply = client_socket.recv(1024)
    reply = reply.decode()

    #print (reply)
    return reply

def lock_file(client_socket, file_path):

    serverName = 'localhost'
    serverPort = 4040   # port of directory service
    client_socket.connect((serverName,serverPort))

    msg = "_1_:" + file_path  # 1 = lock the file

    # send the string requesting file info to directory service
    client_socket.send(msg.encode())
    reply = client_socket.recv(1024)
    reply = reply.decode()

    return reply

def unlock_file(client_socket, file_path):

    serverName = 'localhost'
    serverPort = 4040   # port of directory service
    client_socket.connect((serverName,serverPort))

    msg = "_2_:" + file_path   # 2 = unlock the file

    # send the string requesting file info to directory service
    client_socket.send(msg.encode())
    reply = client_socket.recv(1024)
    reply = reply.decode()

    return reply
  

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