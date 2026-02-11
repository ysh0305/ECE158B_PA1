# Check wether the file exist in the cache
def read_cache(filename):
    filetouse = "/cache/" + filename
    f = open(filetouse[1:], "rb")
    outputdata = f.readlines()
    print('Read from cache')
    return outputdata

# ProxyServer finds a cache hit and generates a response message
def send_cached_response(tcpCliSock, outputdata):
    tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
    tcpCliSock.send(b"Content-Type:text/html\r\n")
    for i in range(0, len(outputdata)):
        tcpCliSock.send(outputdata[i])
    print('Send cache response')


