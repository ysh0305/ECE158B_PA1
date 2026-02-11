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
    print('\nReady to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    # Recieve request
    try:
        message = tcpCliSock.recv(4096).decode()
        if not message:
            tcpCliSock.close()
            continue

        print(message)

        # Extract details from the message
        filename = extract_filename(message)
        method = extract_method(message)
        body = extract_body(message)
        hostn = extract_hostn(filename)

        # If method is GET, check memory structure, then disk.
        # If method is POST, skip cache.
        
        if method == "GET":
            # Flatten name for local storage
            clean_filename = filename.replace("/", "_")

            if filename in cache_log:
                print("Cache Log Hit: File is tracked in memory.")
                try:
                    outputdata = read_cache(filename)
                    send_cached_response(tcpCliSock, outputdata)
                except IOError:
                    # If tracked in memory but missing on disk, fetch again
                    print("Cache inconsistency. Fetching from server...")
                    try:
                        fetch_from_server(hostn, filename, tcpCliSock, method, body)
                    except Exception as e:
                        print(repr(e))
            else:
                # Not in memory structure, treat as cache miss
                print("File not in cache log. Fetching from server...")
                try:
                    fetch_from_server(hostn, filename, tcpCliSock, method, body)
                    cache_log[filename] = clean_filename
                    print(f"Added {filename} to cache log.")

                except Exception as e:
                    print(repr(e))
                    tcpCliSock.send(b"HTTP/1.0 404 Not Found\r\n")
                    tcpCliSock.send(b"Content-Type:text/html\r\n\r\n")
                    tcpCliSock.send(b"<html><body><h1>404 Not Found</h1></body></html>")
        
        elif method == "POST":
            print("POST request detected. Forwarding to server...")
            try:
                fetch_from_server(hostn, filename, tcpCliSock, method, body)
            except Exception as e:
                print(repr(e))
                tcpCliSock.send(b"HTTP/1.0 500 Internal Server Error\r\n\r\n")
        
        else:
            print(f"Method {method} not supported.")

    except Exception as e:
        print("Error processing request:", e)

    # Close the client socket
    tcpCliSock.close()

# Close server socket
tcpSerSock.close()
sys.exit(0)