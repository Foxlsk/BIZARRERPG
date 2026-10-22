import sqlite3
from Database.Database import Database
from Utils.Errors import ValidationError

class Quest:
    Types = ("Hunt", "Explore")
    Difficulties = ("Easy", "Medium", "Hard", "Nightmare")
    Statuses = ("InProgress", "Completed", "Failed")
    Fields = ("Code", "Name", "Description", "Type", "Difficulty", "MinLevel", "Goal", "TargetEnemyId",
              "EnergyCost", "RewardXp", "RewardSouls", "RewardItemId", "RewardItemQuantity", "Active")

    def Init():
        Database.CreateTable("Quests", """
            CREATE TABLE Quests (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Code TEXT NOT NULL UNIQUE,
                Name TEXT NOT NULL UNIQUE,
                Description TEXT NOT NULL,
                Type TEXT NOT NULL CHECK (Type IN ('Hunt', 'Explore')),
                Difficulty TEXT NOT NULL CHECK (Difficulty IN ('Easy', 'Medium', 'Hard', 'Nightmare')),
                MinLevel INTEGER NOT NULL DEFAULT 1 CHECK (MinLevel >= 1),
                Goal INTEGER NOT NULL CHECK (Goal > 0),
                TargetEnemyId INTEGER REFERENCES Enemies(Id) ON DELETE SET NULL,
                EnergyCost INTEGER NOT NULL DEFAULT 0 CHECK (EnergyCost >= 0),
                RewardXp INTEGER NOT NULL DEFAULT 0 CHECK (RewardXp >= 0),
                RewardSouls INTEGER NOT NULL DEFAULT 0 CHECK (RewardSouls >= 0),
                RewardItemId INTEGER REFERENCES Items(Id) ON DELETE SET NULL,
                RewardItemQuantity INTEGER NOT NULL DEFAULT 0 CHECK (RewardItemQuantity >= 0),
                Active INTEGER NOT NULL DEFAULT 1 CHECK (Active IN (0, 1))
            )
        """)

        Database.CreateTable("CharacterQuests", """
            CREATE TABLE CharacterQuests (
                CharacterId INTEGER NOT NULL REFERENCES Characters(Id) ON DELETE CASCADE,
                QuestId INTEGER NOT NULL REFERENCES Quests(Id) ON DELETE CASCADE,
                Status TEXT NOT NULL DEFAULT 'InProgress' CHECK (Status IN ('InProgress', 'Completed', 'Failed')),
                Progress INTEGER NOT NULL DEFAULT 0 CHECK (Progress >= 0),
                AcceptedAt TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                FinishedAt TEXT,
                PRIMARY KEY (CharacterId, QuestId)
            )
        """)

    Select = """
        SELECT q.*, e.Name AS TargetEnemyName, i.Name AS RewardItemName
        FROM Quests q
        LEFT JOIN Enemies e ON e.Id = q.TargetEnemyId
        LEFT JOIN Items i ON i.Id = q.RewardItemId
    """

    def Create(Data, db=None) -> int:
        try:
            return Database.Insert(f"""
                INSERT INTO Quests ({', '.join(Quest.Fields)})
                VALUES ({', '.join(':' + Field for Field in Quest.Fields)})
            """, {Field: Data[Field] for Field in Quest.Fields}, db)
        except sqlite3.IntegrityError:
            raise ValidationError(f"A quest with code '{Data['Code']}' or name '{Data['Name']}' already exists.")

    def Update(Id, Data):
        Params = {Field: Data[Field] for Field in Quest.Fields}
        Params["Id"] = Id
        try:
            Database.Execute(f"""
                UPDATE Quests SET {', '.join(f'{Field} = :{Field}' for Field in Quest.Fields)}
                WHERE Id = :Id
            """, Params)
        except sqlite3.IntegrityError:
            raise ValidationError("Another quest already uses this code or name.")

    def Get(Id, db=None):
        Row = Database.FetchOne(Quest.Select + " WHERE q.Id = ?", (Id,), db)
        return dict(Row) if Row else None

    def GetAll(OnlyActive=False):
        Query = Quest.Select + (" WHERE q.Active = 1" if OnlyActive else "") + " ORDER BY q.MinLevel, q.Id"
        return [dict(Row) for Row in Database.FetchAll(Query)]

    def GetForCharacter(CharacterId):
        """Every active quest with the character's status (Available when there is no progress row)."""
        return [dict(Row) for Row in Database.FetchAll("""
            SELECT q.*, e.Name AS TargetEnemyName, i.Name AS RewardItemName,
                   COALESCE(cq.Status, 'Available') AS Status, COALESCE(cq.Progress, 0) AS Progress
            FROM Quests q
            LEFT JOIN Enemies e ON e.Id = q.TargetEnemyId
            LEFT JOIN Items i ON i.Id = q.RewardItemId
            LEFT JOIN CharacterQuests cq ON cq.QuestId = q.Id AND cq.CharacterId = ?
            WHERE q.Active = 1 OR cq.Status IS NOT NULL
            ORDER BY q.MinLevel, q.Id
        """, (CharacterId,))]

    def GetProgress(CharacterId, QuestId, db=None):
        Row = Database.FetchOne("SELECT * FROM CharacterQuests WHERE CharacterId = ? AND QuestId = ?",
                                (CharacterId, QuestId), db)
        return dict(Row) if Row else None

    def GetInProgress(CharacterId, db=None):
        return [dict(Row) for Row in Database.FetchAll("""
            SELECT q.*, cq.Progress, cq.Status
            FROM CharacterQuests cq
            JOIN Quests q ON q.Id = cq.QuestId
            WHERE cq.CharacterId = ? AND cq.Status = 'InProgress'
        """, (CharacterId,), db)]

    def CountActive(CharacterId, db=None):
        return Database.FetchOne("""
            SELECT COUNT(*) AS Total FROM CharacterQuests WHERE CharacterId = ? AND Status = 'InProgress'
        """, (CharacterId,), db)["Total"]

    def Start(CharacterId, QuestId, db=None):
        Database.Execute("""
            INSERT INTO CharacterQuests (CharacterId, QuestId) VALUES (?, ?)
            ON CONFLICT (CharacterId, QuestId) DO UPDATE
            SET Status = 'InProgress', Progress = 0, AcceptedAt = datetime('now', 'localtime'), FinishedAt = NULL
        """, (CharacterId, QuestId), db)

    def SetProgress(CharacterId, QuestId, Progress, db=None):
        Database.Execute("UPDATE CharacterQuests SET Progress = ? WHERE CharacterId = ? AND QuestId = ?",
                         (Progress, CharacterId, QuestId), db)

    def Finish(CharacterId, QuestId, Status, db=None):
        Database.Execute("""
            UPDATE CharacterQuests SET Status = ?, FinishedAt = datetime('now', 'localtime')
            WHERE CharacterId = ? AND QuestId = ?
        """, (Status, CharacterId, QuestId), db)

Quest.Init();