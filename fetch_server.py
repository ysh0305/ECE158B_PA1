from socket import *

def fetch_from_server(hostn, filename, tcpCliSock):
    # Create a socket on the proxyserver
    c = socket(AF_INET, SOCK_STREAM)

    # Connect to the socket to port 80
    c.connect((hostn, 80))

    # Create a temporary file on this socket and ask port 80 for the file requested by the client
    fileobj = c.makefile('rb', 0)
    c.sendall(("GET "+"http://" + filename + " HTTP/1.0\r\n\r\n").encode())

    # Read the response into buffer
    buffer = fileobj.readlines()
        
    # Create a new file in the cache for the requested file.
    # Also send the response in the buffer to client socket and the corresponding file in the cache
    tmpFile = open("./cache/" + filename,"wb")
    for i in range(0, len(buffer)):
        tcpCliSock.send(buffer[i])
        tmpFile.write(buffer[i])
