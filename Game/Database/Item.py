import json
import sqlite3
from Database.Database import Database
from Utils.Errors import ValidationError

class Item:
    Types = ("Weapon", "Armor", "Potion", "Tool", "Special")
    EquippableTypes = ("Weapon", "Armor", "Special")
    Fields = ("Code", "Name", "Description", "Type", "Price", "Stock", "Effects", "Tradable")

    def Init():
        Database.CreateTable("Items", """
            CREATE TABLE Items (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Code TEXT NOT NULL UNIQUE,
                Name TEXT NOT NULL UNIQUE,
                Description TEXT NOT NULL,
                Type TEXT NOT NULL CHECK (Type IN ('Weapon', 'Armor', 'Potion', 'Tool', 'Special')),
                Price INTEGER NOT NULL CHECK (Price >= 0),
                Stock INTEGER NOT NULL CHECK (Stock >= 0),
                Effects TEXT NOT NULL DEFAULT '{}',
                Tradable INTEGER NOT NULL DEFAULT 1 CHECK (Tradable IN (0, 1))
            )
        """)

    def ToData(Row):
        if Row is None:
            return None
        Data = dict(Row)
        Data["Effects"] = json.loads(Data["Effects"] or "{}")
        Data["Tradable"] = bool(Data["Tradable"])
        return Data

    def Params(Data):
        Params = {Field: Data[Field] for Field in Item.Fields}
        Params["Effects"] = json.dumps(Data["Effects"])
        Params["Tradable"] = 1 if Data["Tradable"] else 0
        return Params

    def Create(Data, db=None) -> int:
        try:
            return Database.Insert("""
                INSERT INTO Items (Code, Name, Description, Type, Price, Stock, Effects, Tradable)
                VALUES (:Code, :Name, :Description, :Type, :Price, :Stock, :Effects, :Tradable)
            """, Item.Params(Data), db)
        except sqlite3.IntegrityError:
            raise ValidationError(f"An item with code '{Data['Code']}' or name '{Data['Name']}' already exists.")

    def Update(Id, Data):
        Params = Item.Params(Data)
        Params["Id"] = Id
        try:
            Database.Execute("""
                UPDATE Items
                SET Code = :Code, Name = :Name, Description = :Description, Type = :Type, Price = :Price,
                    Stock = :Stock, Effects = :Effects, Tradable = :Tradable
                WHERE Id = :Id
            """, Params)
        except sqlite3.IntegrityError:
            raise ValidationError("Another item already uses this code or name.")

    def Delete(Id):
        return Database.Execute("DELETE FROM Items WHERE Id = ?", (Id,))

    def Get(Id, db=None):
        return Item.ToData(Database.FetchOne("SELECT * FROM Items WHERE Id = ?", (Id,), db))

    def GetByCode(Code, db=None):
        return Item.ToData(Database.FetchOne("SELECT * FROM Items WHERE Code = ?", (Code,), db))

    def GetAll(OnlyShop=False):
        Query = "SELECT * FROM Items"
        if OnlyShop:
            Query += " WHERE Tradable = 1"
        Query += " ORDER BY Type, Price"
        return [Item.ToData(Row) for Row in Database.FetchAll(Query)]

    def ChangeStock(Id, Delta, db=None):
        Database.Execute("UPDATE Items SET Stock = Stock + ? WHERE Id = ?", (Delta, Id), db)

Item.Init();