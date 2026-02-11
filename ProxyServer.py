# Skeleton Python Code for the Proxy Server
from socket import *
import sys
from http_parser import *
from cache import *
from fetch_server import *

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(5)

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    # Recieve request
    message = tcpCliSock.recv(4096).decode()
    print(message)

    # Extract the filename from the given message
    filename = extract_filename(message)

    try:
        # Check wether the file exist in the cache
        outputdata = read_cache(filename)

        # ProxyServer finds a cache hit and generates a response message
        send_cached_response(tcpCliSock, outputdata)

    # Error handling for file not found in cache
    except IOError:
        hostn = extract_hostn(filename)
        try:
            fetch_from_server(hostn, filename, tcpCliSock)

        #Print error to debug
        except Exception as e:
            print(repr(e))
            # HTTP response message for file not found
            tcpCliSock.send(b"HTTP/1.0 404 Not Found\r\n")
            tcpCliSock.send(b"Content-Type:text/html\r\n\r\n")
            tcpCliSock.send(b"<html><body><h1>404 Not Found</h1></body></html>")

    # Close the client and the server sockets
    tcpCliSock.close()

# Fill in start.
tcpSerSock.close()
sys.exit(0)
# Fill in end.


