
def open_file(filename, RW):
    
    if RW == "r":
        # check if file to read from exists in the directory
        try:
            file = open(filename, RW)
            return file
        except IOError:
            print (filename + " does not exist in current directory")
            return IOError
            pass
  
    elif RW == "a+":
        file = open(filename, RW)
        print (filename + " is open for writing")
        return file
    

def instructions():
    print ("------------------- INSTRUCTIONS ----------------------")
    print ("<write> [filename] - write to file mode")
    print ("<end> - finish writing")
    print ("<read> [filename] - read a file in your current directory")
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