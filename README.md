# Python Distributed File System 
# CS4400 Internet Applications Individual Project
**Name:** Joseph O'Donovan  
**Student Number:** 14315530

## Dependencies
This project is written in **Python 3.6**  
It was written on a Windows Machine.
This project uses sockets to send information between servers and services.

To run this project, do the following:

* Run the client application: **python client.py**
* Run the directory service: **python directory_service.py**
* Run the locking service: **python locking_service.py**
* Run fileserver A in a separate directory - fileserver A is holds the primary copy for replication and can be written to: **python fileserverA.py**
* Run fileserver B in a separate directory - fileserver B only takes read requests: **python fileserverB.py**
* Run fileserver C in a separate directory - fileserver C (like fileserver B) only takes read requests: **python fileserverC.py**

## Example Usage

* Start up the directory_service.py, the locking_service.py and the three fileservers all in separate terminals. Fileserver A, fileserver B and fileserver c must exist in their own separate folders/ directories.

* Open 2 clients in separate terminals.

* Client 1 write:

```
$<write> file1
You are granted the file...
Write some text...
<end> to finish writing
--------------------------------
$Hello world!
$<end>
--------------------------------
Sending version: 0
File successfully written to
File unlocked...
Exiting <write> mode...

```

* Client 1 read:

```
$<read> file1
Checking version...
Versions match, reading from cache...
--------------------------------
Hello world!

--------------------------------
Exiting <read> mode...
```

* Client 2 read: 

```
$<read> file1
REQUESTING FILE FROM FILE SERVER - FILE NOT IN CACHE
--------------------------------
Hello world!

--------------------------------
file1.txt successfully cached...
Exiting <read> mode...
```

## Project Overview
This project simulates a distributed file system using the NFS protocol.
It can support multiple clients accessing files.
The following are the main components of the file system:

* Distributed transparent file access
* Directory service
* Locking service
* Caching
* Replication

----

**Distributed transparent file access**

Clients can read from and write to files on fileservers. The client side application is a text editor and viewer. The client application's functionality comes from the client library (client_lib.py). The client never downloads or uploads a file from a fileserver, it downloads or uploads the contents of the file. 

The client can use the following commands to access files:

	<write> [filename]  # write to file mode
	<end>           # finish writing
	<read> [filename]   # read from file mode
	<list>          # lists all existing files
	<instructions>      # lets you see the instructions 
	<quit>          # exits the application

----

**Directory service**

A directory service is used to map the file name that the client requests to a file server. The directory service uses a CSV file to store the mappings (file_mappings.csv). This stores the actual name of the file, the file server IP and Port it is stored on and whether the file server is holds the primary copy or not. 

If a client wishes to write to a file the directory service sends the request to fileserver A, the holder of the primary copy. If the client wishes to read from a file the directory service sends the request to fileserver B or fileserver C, these hold replicated versions of the files on fileserver A. 

----

**Locking service**

If client 1 wishes to write to a file it requests to lock the file for writing. Client 1 can only write to a file when it receives the lock, it can read from a file whenever it wants. If client 2 wants to write to a file and the file is locked for writing then client 2 must wait until client 1 has unlocked it. Client 2 who is requesting the write will keep polling to check for the unlocked file. I have included a 10 second timeout for polling (which is a short period of time) for simulation purposes. 

If client 1 is writing to a file and client 2, client 3 and client 4 request to write to the file in this order, client 2 will be the first client to retrieve the lock on the file. When client 2 finishes, client 3 will get the lock, and then client 4, etc. This is fair locking and unlocking. It works as a FIFO queue. 

----

**Caching**

If a client requests to write to a file it goes to the fileserver with the primary copy. The write also goes to the client's cache. The version number of the file is stored on the client side and on the fileserver side. If the client next wishes to read the file, it compares the version number on the fileserver side and the version number on its side. If they match then the client reads from its cache. If they do not match the client reads from the fileserver and updates its record of the version number for the file. This ensures cache consistency between clients.

---- 

**Replication**

The primary copy model is adopted in this file system to implement file replication among fileservers. When a client wishes to write to a file the directory service sends the write to fileserver A. Filserver A holds the primary copy of all files and therefore takes all write requests. When the client finishes writing, fileserver A sends a copy of the file to fileserver B and fileserver C. This ensures consistency of the same files across all fileservers. If a client requests a read it is not sent to fileserver A but is sent to read a replicated copy of the file on fileserver B or fileserver C. 