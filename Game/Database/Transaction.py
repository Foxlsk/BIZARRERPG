from Database.Database import Database

class Transaction:
    Types = ("Buy", "Sell", "Reward", "Penalty")

    def Init():
        Database.CreateTable("Transactions", """
            CREATE TABLE Transactions (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                CharacterId INTEGER NOT NULL REFERENCES Characters(Id) ON DELETE CASCADE,
                ItemId INTEGER REFERENCES Items(Id) ON DELETE SET NULL,
                Type TEXT NOT NULL CHECK (Type IN ('Buy', 'Sell', 'Reward', 'Penalty')),
                Quantity INTEGER NOT NULL DEFAULT 0 CHECK (Quantity >= 0),
                Amount INTEGER NOT NULL CHECK (Amount >= 0),
                BalanceBefore INTEGER NOT NULL CHECK (BalanceBefore >= 0),
                BalanceAfter INTEGER NOT NULL CHECK (BalanceAfter >= 0),
                Description TEXT NOT NULL,
                CreatedAt TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
            )
        """)

    def Add(CharacterId, Type, Amount, BalanceBefore, BalanceAfter, Description, ItemId=None, Quantity=0, db=None):
        return Database.Insert("""
            INSERT INTO Transactions (CharacterId, ItemId, Type, Quantity, Amount, BalanceBefore, BalanceAfter, Description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (CharacterId, ItemId, Type, Quantity, Amount, BalanceBefore, BalanceAfter, Description), db)

    def GetByCharacter(CharacterId, Limit=20):
        return Database.FetchAll("""
            SELECT * FROM Transactions WHERE CharacterId = ? ORDER BY Id DESC LIMIT ?
        """, (CharacterId, Limit))

Transaction.Init();