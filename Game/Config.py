import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

def LoadEnv(Path=ROOT_DIR / ".env"):
    """Loads KEY=VALUE pairs from the .env file (never committed) into os.environ."""
    if not Path.exists():
        return

    for Line in Path.read_text(encoding="utf-8").splitlines():
        Line = Line.strip()
        if not Line or Line.startswith("#") or "=" not in Line:
            continue
        Key, Value = Line.split("=", 1)
        os.environ.setdefault(Key.strip(), Value.strip().strip('"').strip("'"))


LoadEnv()

class Config:
    # Database
    DB_PATH = os.environ.get("PURGATORY_DB_PATH", str(BASE_DIR / "Database" / "Database.db"))
    ADMIN_USERNAME = os.environ.get("PURGATORY_ADMIN_USERNAME")
    ADMIN_EMAIL = os.environ.get("PURGATORY_ADMIN_EMAIL")
    ADMIN_PASSWORD = os.environ.get("PURGATORY_ADMIN_PASSWORD")

    # Character
    STARTING_SOULS = 350
    STARTING_ENERGY = 100
    MAX_LEVEL = 50
    XP_PER_LEVEL = 100

    # Level up bonuses
    LEVEL_UP_HP = 10
    LEVEL_UP_SANITY = 5
    LEVEL_UP_ATTACK = 2
    LEVEL_UP_MAGIC = 2
    LEVEL_UP_DEFENSE = 2
    LEVEL_UP_SPEED = 1

    # Economy
    SELL_RATIO = 0.5

    # Combat
    COMBAT_ENERGY_COST = 10
    BASE_ACCURACY = 0.95
    BASE_CRIT_CHANCE = 0.05
    CRIT_MULTIPLIER = 1.5
    ABILITY_COOLDOWN = 3
    DEFEAT_SOULS_PENALTY = 0.20
    DEFEAT_HP_RECOVERY = 0.25
    OVERLEVEL_GAP = 3

    # Missions
    MAX_ACTIVE_QUESTS = 3
    EXPLORE_FAIL_HP = 10
    EXPLORE_FAIL_SANITY = 10
