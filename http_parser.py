def extract_filename(message):
    # Splits the message to find the URL
    # Example: "GET http://www.google.com HTTP/1.0" -> "www.google.com"
    filename = message.split()[1].replace("http://", "").replace("https://", "").strip("/").split(":")[0]
    print("filename =", filename)
    return filename

def extract_hostn(filename):
    # Extracts the hostname from the filename
    hostn = filename.replace("www.", "", 1).split("/")[0]
    print("hostn =", hostn)
    return hostn

def extract_method(message):
    # Returns "GET", "POST", etc.
    method = message.split()[0]
    print("method =", method)
    return method

def extract_body(message):
    # The body is separated from headers by a double newline (\r\n\r\n)
    parts = message.split("\r\n\r\n", 1)
    if len(parts) > 1:
        return parts[1]
    return ""