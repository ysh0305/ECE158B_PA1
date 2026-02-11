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

cache_log = {}

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
        # Check the internal data structure for a cache hit
        if filename in cache_log:
            print(f"Internal Log Hit: {filename} is tracked.")
            
            try:
                outputdata = read_cache(filename)
                send_cached_response(tcpCliSock, outputdata)
                tcpCliSock.close()
                continue
            except IOError:
                # If in log but file missing from disk, remove from log and proceed to fetch
                print("Inconsistency: Logged file missing from disk. Re-fetching...")
                del cache_log[filename]
            
        else:
            print(f"Internal Log Miss: {filename} not tracked.")
                
    # fetch from server if post or cache miss
    try:
        fetch_from_server(hostn, filename, tcpCliSock, message_byte, method)
        
        # If it was a successful GET fetch, add it to the internal data structure
        if method == "GET":
            cache_log[filename] = True
            print(f"Added to Internal Log: {filename}")
            
    except:
        tcpCliSock.sendall(b"HTTP/1.0 404 Not Found\r\n")
        tcpCliSock.sendall(b"Content-Type:text/html\r\n\r\n")
        tcpCliSock.sendall(b"<html><body><h1>404 Not Found</h1></body></html>")
    tcpCliSock.close()

tcpSerSock.close()
sys.exit(0)


