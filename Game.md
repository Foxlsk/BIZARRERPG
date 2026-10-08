# BIZARRERPG — Game Documentation

## 1. Core Rules & Attribute System

### Player Attributes

* **Health (HP):** Determines physical survival capacity. If it reaches 0, the character is defeated.

* **Sanity (SAN):** Ranges from 0 to 100. Affects perception of the world and combat efficiency.

  * **SAN > 70:** Stable State. No penalties.

  * **30 ≤ SAN ≤ 70:** Disturbed State. 10% chance to fail spiritual abilities.

  * **SAN < 30:** Threshold State. Triggers text hallucinations, enemies deal +20% mental damage, and specific relic effects activate.

  * **SAN = 0:** Madness State. The player loses 10% max HP per turn and suffers -50% Accuracy.

* **Physical Damage (ATK):** Base stat for normal attacks and physical abilities.

* **Spiritual Power (MAG):** Base stat for spells and soul damage.

* **Defense (DEF):** Reduces incoming physical damage.

* **Speed (SPD):** Determines turn order in combat.

* **Accuracy (ACC):** Percentage value (base 100%) determining the chance to hit a target.

### Combat Formulas

* **Physical Damage Taken Calculation:**

  $$
  Damage = \max\left(1, AttackDamage - \lfloor\frac{DEF}{2}\rfloor\right)
  $$

* **Mental Damage Calculation:**
  Mental damage directly depletes **SAN** and ignores player **DEF**.

---

## 2. Character Classes

| Class | Base HP | Base SAN | ATK | MAG | DEF | SPD | Special Ability | Ability Effect |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Iron Penitent** | 150 | 60 | 20 | 5 | 25 | 8 | *Martyrdom of the Flesh* | Converts 50% of physical damage taken in the last turn into an ATK bonus for the next attack. |
| **Shadow Reaper** | 80 | 80 | 25 | 15 | 10 | 20 | *Essence Sever* | Ignores enemy DEF and deals $1.5 \times ATK$ as direct soul damage. |
| **Ash Bearer** | 100 | 100 | 10 | 30 | 15 | 12 | *Shroud of Oblivion* | Reduces enemy ACC by 30% and restores 15 SAN to the party over 2 turns. |
| **Blind Inquisitor**| 110 | 120 | 18 | 20 | 20 | 15 | *Abyssal Perception* | Reveals target weak point: increases all damage taken by the target by +35% for 3 turns. |

---

## 3. Item and Consumable Catalog

### Consumables

| ID | Name | Type | Concrete Effect | Cost / Value |
| :--- | :--- | :--- | :--- | :--- |
| `item_ether_tear` | Ether Tear | Consumable | Restores +30 SAN; Removes the *Disturbed* state. | 25 Souls |
| `item_cold_elixir`| Cold Ash Elixir | Consumable | Restores +40 HP; Applies -10% SPD on the next turn. | 20 Souls |
| `item_soul_shard` | Barbed Soul Shard| Consumable | Grants +25% MAG for 3 turns; Deals 5 direct damage to user's HP. | 40 Souls |

### Relics and Equipment

| ID | Name | Type | Passive Effect |
| :--- | :--- | :--- | :--- |
| `eq_penitent_chain`| Penitent's Chain | Equipment | Grants +15 DEF when current SAN drops below 30. |
| `eq_obsidian_eye` | Obsidian Eye | Equipment | Prevents ambushes and increases user ACC by +15%. |
| `eq_brass_bell` | Corroded Brass Bell| Equipment | Draws all enemy aggression and grants a shield equal to 20% Max HP. |

### Key Items

| ID | Name | Type | Description |
| :--- | :--- | :--- | :--- |
| `key_seal_forgotten`| Seal of the Forgotten | Key Item | Required to unlock the gates to Level 2 of Purgatory. |

---

## 4. Bestiary (Enemies and Bosses)

### Common Enemies

#### Wraith of Guilt
* **HP:** 50 | **DEF:** 5 | **SPD:** 18
* **Physical Attack:** 5 damage
* **Ability — *Abyssal Whisper*:** Deals 15 Mental Damage and reduces player ACC by 20% for 2 turns.

#### Petrified Warrior
* **HP:** 120 | **DEF:** 25 | **SPD:** 5
* **Physical Attack:** 15 damage
* **Ability — *Ground Slam*:** Deals 25 Physical Damage (ignores 50% of player DEF).

### Zone Boss

#### Corrupted Commander
* **Phase 1:** HP 250 | DEF 15 | SPD 12
  * **Physical Attack:** 30 damage with corrupted blade.
  * **Ability — *War Lament*:** Increases own ATK by +20% and forces player to skip 1 turn due to shock.
* **Phase 2 (Triggers at 50% HP):** HP 125 | DEF 10 | SPD 16
  * **Abyssal Aura:** Deals 8 Mental Damage and 5 Physical Damage to all players at the start of each turn.

---

## 5. NPCs and Interaction Table

| NPC | Role | Service Cost | Available Action |
| :--- | :--- | :--- | :--- |
| **The Blind Occultist** | Abyssal Merchant | -10 Max SAN | Trade for rare items and advanced consumables. |
| **The Keeper of Grief** | Guide & Rest Point | Free | Fully restores HP and SAN; Allows saving progress. |
| **The Broken Blacksmith**| Forger | 50 Souls + 2 Essences | Increases weapon ATK by +5 or armor DEF by +5. |

---

## 6. Quest Table

```json
[
  {
    "id": "quest_main_01",
    "title": "Rescue of the Echo",
    "type": "Main",
    "objective": "Defeat the Corrupted Commander",
    "max_progress": 1,
    "rewards": {
      "item": "key_seal_forgotten",
      "xp": 150
    }
  },
  {
    "id": "quest_side_01",
    "title": "The Broken Vow",
    "type": "Side",
    "objective": "Purify the 3 Altars of Penitence",
    "max_progress": 3,
    "rewards": {
      "item": "eq_penitent_chain",
      "restore_sanity": true
    }
  },
  {
    "id": "quest_hunt_01",
    "title": "The Unquenchable Flame",
    "type": "Gathering",
    "objective": "Collect 5 Cold Ash Essences from Ash Wraiths",
    "max_progress": 5,
    "rewards": {
      "item": "item_ether_tear",
      "quantity": 2
    }
  }
]
```