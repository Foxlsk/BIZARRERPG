import hashlib

def Hash(input):
    hash = hashlib.sha256()
    hash.update(str.encode(input))
    return hash.hexdigest();