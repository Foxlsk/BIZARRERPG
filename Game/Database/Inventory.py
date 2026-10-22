import json
from Database.Database import Database

class Inventory:
    BonusKeys = ("Attack", "Magic", "Defense", "Speed", "Accuracy", "ExploreBonus", "FleeBonus")

    def Init():
        Database.CreateTable("Inventory", """
            CREATE TABLE Inventory (
                CharacterId INTEGER NOT NULL REFERENCES Characters(Id) ON DELETE CASCADE,
                ItemId INTEGER NOT NULL REFERENCES Items(Id) ON DELETE CASCADE,
                Quantity INTEGER NOT NULL CHECK (Quantity > 0),
                Equipped INTEGER NOT NULL DEFAULT 0 CHECK (Equipped IN (0, 1)),
                AcquiredAt TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                PRIMARY KEY (CharacterId, ItemId)
            )
        """)

    def ToData(Row):
        Data = dict(Row)
        Data["Effects"] = json.loads(Data["Effects"] or "{}")
        Data["Equipped"] = bool(Data["Equipped"])
        Data["Tradable"] = bool(Data["Tradable"])
        return Data

    def GetAll(CharacterId, db=None):
        Rows = Database.FetchAll("""
            SELECT i.Id, i.Code, i.Name, i.Description, i.Type, i.Price, i.Effects, i.Tradable,
                   inv.Quantity, inv.Equipped
            FROM Inventory inv
            JOIN Items i ON i.Id = inv.ItemId
            WHERE inv.CharacterId = ?
            ORDER BY i.Type, i.Name
        """, (CharacterId,), db)
        return [Inventory.ToData(Row) for Row in Rows]

    def Get(CharacterId, ItemId, db=None):
        Row = Database.FetchOne("""
            SELECT i.Id, i.Code, i.Name, i.Description, i.Type, i.Price, i.Effects, i.Tradable,
                   inv.Quantity, inv.Equipped
            FROM Inventory inv
            JOIN Items i ON i.Id = inv.ItemId
            WHERE inv.CharacterId = ? AND inv.ItemId = ?
        """, (CharacterId, ItemId), db)
        return Inventory.ToData(Row) if Row else None

    def Add(CharacterId, ItemId, Quantity, db=None):
        Database.Execute("""
            INSERT INTO Inventory (CharacterId, ItemId, Quantity) VALUES (?, ?, ?)
            ON CONFLICT (CharacterId, ItemId) DO UPDATE SET Quantity = Quantity + excluded.Quantity
        """, (CharacterId, ItemId, Quantity), db)

    def Remove(CharacterId, ItemId, Quantity, db=None):
        with Database.Use(db) as con:
            Row = con.execute("SELECT Quantity FROM Inventory WHERE CharacterId = ? AND ItemId = ?",
                              (CharacterId, ItemId)).fetchone()
            if Row is None or Row["Quantity"] < Quantity:
                return False
            if Row["Quantity"] == Quantity:
                con.execute("DELETE FROM Inventory WHERE CharacterId = ? AND ItemId = ?", (CharacterId, ItemId))
            else:
                con.execute("UPDATE Inventory SET Quantity = Quantity - ? WHERE CharacterId = ? AND ItemId = ?",
                            (Quantity, CharacterId, ItemId))
            return True

    def SetEquipped(CharacterId, ItemId, Equipped, db=None):
        Database.Execute("UPDATE Inventory SET Equipped = ? WHERE CharacterId = ? AND ItemId = ?",
                         (1 if Equipped else 0, CharacterId, ItemId), db)

    def UnequipType(CharacterId, Type, db=None):
        Database.Execute("""
            UPDATE Inventory SET Equipped = 0
            WHERE CharacterId = ? AND ItemId IN (SELECT Id FROM Items WHERE Type = ?)
        """, (CharacterId, Type), db)

    def GetBonuses(CharacterId, db=None):
        """Sums the effects of equipped gear and carried tools."""
        Rows = Database.FetchAll("""
            SELECT i.Effects
            FROM Inventory inv
            JOIN Items i ON i.Id = inv.ItemId
            WHERE inv.CharacterId = ? AND (inv.Equipped = 1 OR i.Type = 'Tool')
        """, (CharacterId,), db)

        Bonuses = {Key: 0 for Key in Inventory.BonusKeys}
        for Row in Rows:
            for Key, Value in json.loads(Row["Effects"] or "{}").items():
                if Key in Bonuses:
                    Bonuses[Key] += Value
        return Bonuses

Inventory.Init()