
def extract_filename(message):
    filename = message.split()[1].replace("http://", "").replace("https://", "").strip("/").split(":")[0]
    print("filename =", filename)
    return filename

def extract_hostn(filename):
    hostn = filename.replace("www.", "", 1).split("/")[0]
    print("hostn =", hostn)
    return hostn

def recv_http_request(sock):

    data = sock.recv(4096)
    message = data.decode()

    # get method from header
    method = message.split()[0]

    # If POST read the body
    if method == "POST":
        header_end = data.find(b"\r\n\r\n")
        headers = message[:header_end]

        # find Content-Length
        length = 0
        for line in headers.split("\r\n"):
            if line.lower().startswith("content-length:"):
                length = int(line.split(":", 1)[1].strip())
                break

        # how many body bytes we already have
        body = len(data) - (header_end + 4)

        # read remaining body bytes if needed
        while body < length:
            chunk = sock.recv(min(4096, length - body))
            if not chunk:
                break
            data += chunk
            body += len(chunk)

        # decode full request with body
        message = data.decode()

    return data, message, method

# Process response: end recieving after the content length match the header to avoid hanging
def recv_http_response(sock):
    data = sock.recv(4096)
    message = data.decode()

    # find end of headers
    header_end = data.find(b"\r\n\r\n")
    if header_end == -1:
        return data, message

    headers = message[:header_end]

    # find length
    length = 0
    for line in headers.split("\r\n"):
        if line.lower().startswith("content-length:"):
            length = int(line.split(":", 1)[1].strip())
            break

    # how many body bytes already received
    body = len(data) - (header_end + 4)

    # read remaining body bytes if needed
    while body < length:
        chunk = sock.recv(min(4096, length - body))
        if not chunk:
            break
        data += chunk
        body += len(chunk)

    return data
