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
    print("\n\n--------------------------\n Ready to Serve \n--------------------------")
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    # Recieve request
    message_byte, message, method = recv_http_request(tcpCliSock)
    print(message)

    # Extract the filename from the given message
    filename = extract_filename(message)
    hostn = extract_hostn(filename)

    # Only check cache if the method is GET
    if method == "GET":
        try:
            outputdata = read_cache(filename)
            send_cached_response(tcpCliSock, outputdata)
            tcpCliSock.close()
            continue
        except IOError:
            pass  # cache miss
    
    # fetch from server if post or cache miss
    try:
        fetch_from_server(hostn, filename, tcpCliSock, message_byte, method)
    except:
        tcpCliSock.sendall(b"HTTP/1.0 404 Not Found\r\n")
        tcpCliSock.sendall(b"Content-Type:text/html\r\n\r\n")
        tcpCliSock.sendall(b"<html><body><h1>404 Not Found</h1></body></html>")
    tcpCliSock.close()

tcpSerSock.close()
sys.exit(0)


