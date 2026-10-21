import json
from pathlib import Path

class ResourcesHelper:
    BasePath = Path(__file__).resolve().parent.parent / "Resources"

    def Load(Name):
        with open(ResourcesHelper.BasePath / f"{Name}.json", 'r', encoding="utf-8") as file:
            return json.load(file)