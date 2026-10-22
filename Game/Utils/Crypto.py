import hashlib

class CryptoUtils:
    salt = "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b"
    def Hash(input):
        hash = hashlib.sha256()
        hash.update(str.encode(f"{input}-{CryptoUtils.salt}"))
        return hash.hexdigest();

    def Verify(input, hash):
        return CryptoUtils.Hash(input) == hash;