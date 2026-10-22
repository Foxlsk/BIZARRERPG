from dataclasses import dataclass

@dataclass
class Combatant:
    Name: str
    HP: int
    MaxHP: int
    Attack: int
    Defense: int
    Speed: int
    Magic: int = 0
    Accuracy: float = 0.9
    CritChance: float = 0.05
    DodgeChance: float = 0.0
    Sanity: int = 0
    MaxSanity: int = 0

    def IsAlive(self):
        return self.HP > 0

    def TakeDamage(self, Amount):
        Dealt = min(self.HP, max(0, Amount))
        self.HP -= Dealt
        return Dealt

    def Heal(self, Amount):
        Before = self.HP
        self.HP = max(1, min(self.MaxHP, self.HP + Amount))
        return self.HP - Before

    def LoseSanity(self, Amount):
        Lost = min(self.Sanity, max(0, Amount))
        self.Sanity -= Lost
        return Lost

    def RestoreSanity(self, Amount):
        Before = self.Sanity
        self.Sanity = min(self.MaxSanity, self.Sanity + Amount)
        return self.Sanity - Before
