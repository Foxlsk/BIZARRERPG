from Database.Database import Database;
from Utils.Crypto import CryptoUtils;

class Account:
    def Init():
        if not Database.TableExists("Users"):
            print("[Account] Creating Users Table")
        else:
            print("[Account] Users Loaded")

    def Create(Email, Password):
        print(CryptoUtils.Hash(Password));

Account.Init();