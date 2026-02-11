
def extract_filename(message):
    filename = message.split()[1].replace("http://", "").replace("https://", "").strip("/").split(":")[0]
    print("filename =", filename)
    return filename

def extract_hostn(filename):
    hostn = filename.replace("www.", "", 1).split("/")[0]
    print("hostn =", hostn)
    return hostn
