from Database.Database import Database;
from Utils.Crypto import CryptoUtils;
from typing import TypedDict

class AccountData(TypedDict):
    Id: int
    Username: str
    Email: str
    Password: str
    Role: str
    Created: str

class Account:
    def Init():
        Database.CreateTable("Users", """
            CREATE TABLE Users (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE,
                Email TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL,
                Role TEXT NOT NULL,
                CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def Create(Username, Email, Password):
        HashedPassword = CryptoUtils.Hash(Password)
        print(f"[Account] Creating User | Username: {Username}, Email: {Email}, Password: {HashedPassword}");
        try:
            Database.Execute("""
                        INSERT INTO Users (Username, Email, Password, Role)
                        VALUES (?, ?, ?, ?)
                    """, (Username, Email, HashedPassword, "Player"))
            print("[Account] Success.")
        except:
            print(f"[Account] Failed (Account w Username: {Username} or Email: {Email} already exist).")

    def Get(Id) -> AccountData | None:
        try:
            User = Database.FetchOne("""
                SELECT * FROM Users WHERE Id = ?
            """, (Id,))
            return {
                "Id": User[0],
                "Username": User[1],
                "Email": User[2],
                "Password": User[3],
                "Role": User[4],
                "Created": User[5]
            }
        except: 
            return;

Account.Init();