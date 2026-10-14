
import json
from pathlib import Path

class PlayerHelper:
    PlayerResources = {}

    def Init():
        base_path = Path(__file__).resolve().parent.parent
        player_path = base_path / "Resources" / "Player.json"
        with open(player_path, "r", encoding="utf-8") as file:
            PlayerHelper.PlayerResources = json.load(file)

    def GetPlayerPerks(Role):
        for role in PlayerHelper.PlayerResources.get("Roles", []):
            if role["Name"].lower() == Role.lower():
                return role["Perks"]

        return []

    def HashPerk(Role, Perk):
        perks = PlayerHelper.GetPlayerPerks(Role);
        return Perk in perks or "All" in perks;


PlayerHelper.Init()