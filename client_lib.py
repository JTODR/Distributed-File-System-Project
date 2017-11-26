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
    #print ("SENT " + send_msg + " to " + str(fileserverIP_DS) + " " + str(fileserverPORT_DS))

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

def lock_unlock_file(client_socket, client_id, file_path, lock_or_unlock):

    serverName = 'localhost'
    serverPort = 4040   # port of directory service
    client_socket.connect((serverName,serverPort))

    if lock_or_unlock == "lock":
        msg = client_id + "_1_:" + file_path  # 1 = lock the file
    elif lock_or_unlock == "unlock":
        msg = client_id + "_2_:" + file_path   # 2 = unlock the file

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
    print ("<quit> - exits the application")
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