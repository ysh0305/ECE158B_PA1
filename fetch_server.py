from socket import *

def fetch_from_server(hostn, filename, tcpCliSock, method, body):
    try:
        # Create a socket on the proxyserver
        c = socket(AF_INET, SOCK_STREAM)

        # Connect to the socket to port 80
        c.connect((hostn, 80))

        # Create the request line
        request_line = f"{method} http://{filename} HTTP/1.0\r\n"
        
        # Build headers
        headers = ""
        if method == "POST":
            headers += f"Content-Length: {len(body)}\r\n"
            headers += "Content-Type: application/x-www-form-urlencoded\r\n"
        
        headers += "\r\n"

        # Send request
        full_request = request_line + headers + body
        c.sendall(full_request.encode())

        # Read the response into buffer
        fileobj = c.makefile('rb', 0)
        buffer = fileobj.readlines()
            
        if method == "GET":
            # Flatten the filename so we don't need subdirectories
            clean_filename = filename.replace("/", "_")
            
            # Save to cache using the flattened name
            tmpFile = open("./cache/" + clean_filename, "wb")
            for i in range(0, len(buffer)):
                tcpCliSock.send(buffer[i])
                tmpFile.write(buffer[i])
            tmpFile.close()
            print("File fetched from server and cached.")
        else:
            # For POST, just forward the response
            for i in range(0, len(buffer)):
                tcpCliSock.send(buffer[i])
            print("POST response forwarded (not cached).")
            
        c.close()

    except Exception as e:
        print("Error in fetch_from_server:", e)