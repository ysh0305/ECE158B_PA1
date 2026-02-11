from socket import *
from http_parser import *
def fetch_from_server(hostn, filename, tcpCliSock, message_byte, method):
    # Create a socket on the proxyserver
    c = socket(AF_INET, SOCK_STREAM)
    
    # Connect to the socket to port 80
    c.connect((hostn, 80))

    # Forward the request to the server
    c.sendall(message_byte)

    # Create a new file in the cache for the requested file ONLY if request is GET
    # Also send the response to client socket and the corresponding file in the cache
    if method == "GET":
        tmpFile = open("./cache/" + filename, "wb")
    else:
        tmpFile = None
    
    # modify the template to fix the isssue where the response take long time to process
    response = recv_http_response(c)
    tcpCliSock.sendall(response)
    
    if tmpFile:
        tmpFile.write(response)
        tmpFile.close()

    c.close()
