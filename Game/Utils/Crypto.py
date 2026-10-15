import hashlib

class CryptoUtils:
    def Hash(input):
        hash = hashlib.sha256()
        hash.update(str.encode(input))
        return hash.hexdigest();