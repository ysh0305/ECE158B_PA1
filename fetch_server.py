from socket import *

def fetch_from_server(hostn, filename, tcpCliSock, message_byte, method):
    # Create a socket on the proxyserver
    c = socket(AF_INET, SOCK_STREAM)
    
    # Connect to the socket to port 80
    c.connect((hostn, 80))

    print("before send")
    # Forward the request to the server
    c.sendall(message_byte)

    print("create file")
    # Create a new file in the cache for the requested file ONLY if request is GET
    # Also send the response to client socket and the corresponding file in the cache
    if method == "GET":
        tmpFile = open("./cache/" + filename, "wb")
    else:
        tmpFile = None
    
    print("sending")
    # modify the template to fix the isssue where the response take long time to process
    while True:
        data = c.recv(4096)
        if not data:
            c.close()
            break
        tcpCliSock.sendall(data)
        if tmpFile:
            tmpFile.write(data)

    if tmpFile:
        tmpFile.close()
