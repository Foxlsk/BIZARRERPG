import sqlite3
from Config import Config
from Database.Database import Database
from Models.Character import PlayerCharacter
from Utils.Errors import ValidationError

class Character:
    Select = """
        SELECT c.*, cl.Name AS ClassName
        FROM Characters c
        JOIN Classes cl ON cl.Id = c.ClassId
    """

    def Init():
        Database.CreateTable("Characters", """
            CREATE TABLE Characters (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId INTEGER NOT NULL UNIQUE REFERENCES Users(Id) ON DELETE CASCADE,
                ClassId INTEGER NOT NULL REFERENCES Classes(Id),
                Name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                Level INTEGER NOT NULL DEFAULT 1 CHECK (Level >= 1),
                Xp INTEGER NOT NULL DEFAULT 0 CHECK (Xp >= 0),
                HP INTEGER NOT NULL CHECK (HP >= 0),
                MaxHP INTEGER NOT NULL CHECK (MaxHP > 0),
                Sanity INTEGER NOT NULL CHECK (Sanity >= 0),
                MaxSanity INTEGER NOT NULL CHECK (MaxSanity > 0),
                Energy INTEGER NOT NULL CHECK (Energy >= 0),
                MaxEnergy INTEGER NOT NULL CHECK (MaxEnergy > 0),
                Souls INTEGER NOT NULL CHECK (Souls >= 0),
                Attack INTEGER NOT NULL CHECK (Attack >= 0),
                Magic INTEGER NOT NULL CHECK (Magic >= 0),
                Defense INTEGER NOT NULL CHECK (Defense >= 0),
                Speed INTEGER NOT NULL CHECK (Speed >= 0),
                Wins INTEGER NOT NULL DEFAULT 0 CHECK (Wins >= 0),
                Losses INTEGER NOT NULL DEFAULT 0 CHECK (Losses >= 0),
                CreatedAt TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                CHECK (HP <= MaxHP),
                CHECK (Sanity <= MaxSanity),
                CHECK (Energy <= MaxEnergy)
            )
        """)

    def Create(UserId, Class, Name) -> int:
        try:
            return Database.Insert("""
                INSERT INTO Characters (UserId, ClassId, Name, HP, MaxHP, Sanity, MaxSanity, Energy, MaxEnergy,
                                        Souls, Attack, Magic, Defense, Speed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (UserId, Class["Id"], Name, Class["BaseHP"], Class["BaseHP"], Class["BaseSanity"], Class["BaseSanity"],
                  Config.STARTING_ENERGY, Config.STARTING_ENERGY, Config.STARTING_SOULS,
                  Class["Attack"], Class["Magic"], Class["Defense"], Class["Speed"]))
        except sqlite3.IntegrityError:
            raise ValidationError("This account already has a character or the name is already taken.")

    def ToModel(Row) -> PlayerCharacter | None:
        return PlayerCharacter.FromRow(Row) if Row else None

    def Get(Id, db=None) -> PlayerCharacter | None:
        return Character.ToModel(Database.FetchOne(Character.Select + " WHERE c.Id = ?", (Id,), db))

    def GetByUser(UserId, db=None) -> PlayerCharacter | None:
        return Character.ToModel(Database.FetchOne(Character.Select + " WHERE c.UserId = ?", (UserId,), db))

    def GetByName(Name) -> PlayerCharacter | None:
        return Character.ToModel(Database.FetchOne(Character.Select + " WHERE c.Name = ?", (Name,)))

    def Save(Model: PlayerCharacter, db=None):
        Database.Execute("""
            UPDATE Characters
            SET Level = ?, Xp = ?, HP = ?, MaxHP = ?, Sanity = ?, MaxSanity = ?, Energy = ?, MaxEnergy = ?,
                Souls = ?, Attack = ?, Magic = ?, Defense = ?, Speed = ?, Wins = ?, Losses = ?
            WHERE Id = ?
        """, (Model.Level, Model.Xp, Model.HP, Model.MaxHP, Model.Sanity, Model.MaxSanity, Model.Energy,
              Model.MaxEnergy, Model.Souls, Model.Attack, Model.Magic, Model.Defense, Model.Speed,
              Model.Wins, Model.Losses, Model.Id), db)


Character.Init();