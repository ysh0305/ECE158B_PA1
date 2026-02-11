# Check wether the file exist in the cache
def read_cache(filename):
    # Replace slashes with underscores to avoid directory conflicts
    clean_filename = filename.replace("/", "_")
    
    filetouse = "./cache/" + clean_filename
    try:
        f = open(filetouse, "rb")
        outputdata = f.readlines()
        print('Read from cache')
        return outputdata
    except IOError:
        raise IOError

# ProxyServer finds a cache hit and generates a response message
def send_cached_response(tcpCliSock, outputdata):
    for line in outputdata:
        tcpCliSock.send(line)
    print('Send cache response')