# Guide — Figma / ThePurgatory

## Figma Community link

https://www.figma.com/community/file/1690327958319187452

## How to use the Community file

1. Open the link above and sign in to Figma.
2. Click **Open in Figma** (or **Duplicate**) to copy the file into your *Drafts*.
3. Always work on your copy: the original Community file is not editable.
4. Rename the file (e.g. `ThePurgatory - Design`) and move it to your project or team.

## Using it with the ThePurgatory ER diagram

The ER diagram was generated in FigJam (`ThePurgatory Entity-Relationship Diagram`) with these entities:

| Entity | Description |
|---|---|
| `PLAYER` | Player (HP, SAN, Souls, XP) |
| `CHARACTER_CLASS` | Classes: Iron Penitent, Shadow Reaper, Ash Bearer, Blind Inquisitor |
| `ITEM` | Consumables, equipment and key items |
| `ENEMY` / `BOSS_PHASE` | Bestiary and boss phases |
| `NPC` / `NPC_ITEM` | NPCs and the items they sell |
| `QUEST` / `PLAYER_QUEST` | Quests and player progress |
| `PLAYER_ITEM` | Player inventory |

To integrate:

1. Open the ER diagram in FigJam.
2. Copy the diagram (`Ctrl/Cmd + C`) and paste it into the documentation page of the duplicated file.
3. Keep entity names identical to the database / game documentation.

## Notes

- Whenever the game documentation changes (attributes, items, quests), update the ER diagram.
- Layout edits (moving boxes, fonts) are done directly in Figma/FigJam.