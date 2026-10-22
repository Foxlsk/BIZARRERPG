from dataclasses import dataclass, fields
from Config import Config
from Utils.Errors import GameError, InsufficientFunds

@dataclass
class PlayerCharacter:
    Id: int
    UserId: int
    ClassId: int
    ClassName: str
    Name: str
    Level: int
    Xp: int
    HP: int
    MaxHP: int
    Sanity: int
    MaxSanity: int
    Energy: int
    MaxEnergy: int
    Souls: int
    Attack: int
    Magic: int
    Defense: int
    Speed: int
    Wins: int
    Losses: int
    CreatedAt: str

    @classmethod
    def FromRow(cls, Row):
        return cls(**{Field.name: Row[Field.name] for Field in fields(cls)})

    # Experience: reaching level L requires 50 * L * (L - 1) total XP (100, 300, 600, 1000, ...)
    def TotalXpForLevel(Level):
        return Config.XP_PER_LEVEL * Level * (Level - 1) // 2

    def XpIntoLevel(self):
        return self.Xp - PlayerCharacter.TotalXpForLevel(self.Level)

    def XpForNextLevel(self):
        return Config.XP_PER_LEVEL * self.Level

    def GainXp(self, Amount) -> int:
        """Adds XP and levels up as many times as needed. Returns the number of levels gained."""
        if Amount < 0:
            raise ValueError("XP amount cannot be negative.")

        self.Xp += Amount
        Gained = 0
        while self.Level < Config.MAX_LEVEL and self.Xp >= PlayerCharacter.TotalXpForLevel(self.Level + 1):
            self.Level += 1
            self.ApplyLevelUp()
            Gained += 1
        return Gained

    def ApplyLevelUp(self):
        self.MaxHP += Config.LEVEL_UP_HP
        self.MaxSanity += Config.LEVEL_UP_SANITY
        self.Attack += Config.LEVEL_UP_ATTACK
        self.Magic += Config.LEVEL_UP_MAGIC
        self.Defense += Config.LEVEL_UP_DEFENSE
        self.Speed += Config.LEVEL_UP_SPEED
        self.HP = self.MaxHP
        self.Sanity = self.MaxSanity

    def Heal(self, Amount):
        Before = self.HP
        self.HP = max(1 if Before > 0 else 0, min(self.MaxHP, self.HP + Amount))
        return self.HP - Before

    def RestoreSanity(self, Amount):
        Before = self.Sanity
        self.Sanity = max(0, min(self.MaxSanity, self.Sanity + Amount))
        return self.Sanity - Before

    def RestoreEnergy(self, Amount):
        Before = self.Energy
        self.Energy = max(0, min(self.MaxEnergy, self.Energy + Amount))
        return self.Energy - Before

    def SpendEnergy(self, Amount):
        if self.Energy < Amount:
            raise GameError(f"Not enough energy ({self.Energy}/{Amount}). Rest at the Keeper of Grief.")
        self.Energy -= Amount

    def SpendSouls(self, Amount):
        if self.Souls < Amount:
            raise InsufficientFunds(f"Not enough souls. You have {self.Souls}, need {Amount}.")
        self.Souls -= Amount

    def EarnSouls(self, Amount):
        self.Souls += Amount

    def SanityState(self):
        if self.Sanity == 0:
            return "Madness"
        if self.Sanity < 30:
            return "Threshold"
        if self.Sanity <= 70:
            return "Disturbed"
        return "Stable"
