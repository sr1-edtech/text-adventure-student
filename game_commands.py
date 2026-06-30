# ===========================================================================
#  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗
#  ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝
#  ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗
#  ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║
#  ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║
#   ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝
#
#  YOUR FILE — write your commands here
# ===========================================================================

import game_engine as ge


# ============================================================
#  PARSING
# ============================================================

def parse_command(raw):
    """Split raw input into (verb, noun). Both lowercase."""
    words = raw.lower().strip().split()
    if not words:
        return None, None
    verb = words[0]
    noun = " ".join(words[1:]) if len(words) > 1 else None
    return verb, noun


# ============================================================
#  COMMANDS
# ============================================================

def cmd_go(noun, game):
    """Move in a direction — blocked by living enemies or hidden exits."""
    room = ge.get_room(game)

    if noun is None:
        return ("error", "Go where? Try: go north, south, east, west.")

    if game["player"]["location"] == "ocean_middle" and noun == "north":
        if not game["player"].get("parchment_read", False):
            return ("error",
                    "You stare into the darkness. The stars above form a pattern "
                    "you almost recognise — like a constellation you should know. "
                    "Your parchment might hold the answer. Type 'read parchment'.")

    if noun not in room["exits"]:
        valid = ", ".join(room["exits"].keys())
        return ("error", f"You can't go {noun} from here. Exits: {valid}.")

    if ge.room_is_blocked(game):
        enemy, _ = ge.get_enemy_in_room(game)
        return ("error",
                f"You can't leave while the {enemy['name']} is alive! "
                f"Type 'attack' to fight it.")

    game["player"]["location"] = room["exits"][noun]
    game["player"]["moves"] += 1

    _, arrival_desc = cmd_look(None, game)
    return ("response", f"You head {noun}.\n\n{arrival_desc}")


def cmd_look(noun, game):
    """Look around the room."""
    room = ge.get_room(game)
    location = game["player"]["location"]

    if noun is None or noun in ["around", "room", "here"]:

        if location == "cave":
            has_light = "lantern" in game["player"]["inventory"]
            if not has_light:
                desc = room["description"]
                desc += "\n\nIt is pitch black. You need a lantern to see anything."
                exits = ", ".join(room["exits"].keys())
                desc += f"\n\nExits: {exits}."
                return ("response", desc)
            elif not room.get("chest_locked", True):
                desc = room["description_open"]
            else:
                desc = room["description_lit"]
        else:
            desc = room["description"]

        if room["items"]:
            names = ", ".join(room["items"])
            desc += f"\n\nOn the ground: {names}."

        for eid in room.get("enemies", []):
            enemy = game["enemies"].get(eid, {})
            if enemy.get("alive", False):
                edesc = enemy.get("description", enemy["name"])
                desc += f"\n\n[ALERT] {edesc}"

        if location == "ocean_middle" and not game["player"].get("parchment_read", False):
            visible_exits = {k: v for k, v in room["exits"].items() if k != "north"}
            exits = ", ".join(visible_exits.keys())
            desc += f"\n\nExits: {exits}."
            desc += "\n\nThe stars above seem to form a pattern. Perhaps your parchment holds a clue."
        else:
            exits = ", ".join(room["exits"].keys())
            desc += f"\n\nExits: {exits}."

        return ("response", desc)

    return ("error", "Try: look, or examine <item> to inspect something.")


def cmd_pick(noun, game):
    """Pick up an item from the current room."""
    room = ge.get_room(game)
    location = game["player"]["location"]

    if location == "cave" and "lantern" not in game["player"]["inventory"]:
        return ("error", "It's too dark to find anything. You need a lantern.")

    if ge.room_is_blocked(game):
        enemy, _ = ge.get_enemy_in_room(game)
        return ("error",
                f"You can't do that while the {enemy['name']} is alive! Defeat it first.")

    if noun is None:
        return ("error", "Pick up what?")
    if noun not in room["items"]:
        return ("error", f"There's no '{noun}' here.")
    if not game["items"].get(noun, {}).get("takeable", True):
        return ("error", f"You can't pick up the {noun}.")

    if len(game["player"]["inventory"]) >= 3:
        inv = ", ".join(game["player"]["inventory"])
        return ("error",
                f"Your pack is full (max 3 items). "
                f"Carrying: {inv}. Drop something first.")

    room["items"].remove(noun)
    game["player"]["inventory"].append(noun)

    if noun == "grimoire":
        game["player"]["score"] += 100
        return ("response",
                "You reach out and take the grimoire.\n\n"
                "The moment your hands touch it, the constellations on its cover shift — "
                "rearranging into the same stars that guided you north.\n\n"
                "The title reveals itself: The Grimoire of Wisdom.\n\n"
                "You open it. The first page reads:\n"
                "  'Python Programming: From Zero to Adventure'\n\n"
                "You turn the page. Another chapter appears, freshly written.\n"
                "It already knows what you need to learn next.\n\n"
                f"✨ YOU WIN. Final score: {game['player']['score']}. "
                "Type 'restart' to play again.")

    return ("response", f"You pick up the {noun}.")


def cmd_drop(noun, game):
    """Drop an item from inventory into the current room."""
    room = ge.get_room(game)
    if noun is None:
        return ("error", "Drop what?")
    if noun not in game["player"]["inventory"]:
        return ("error", f"You're not carrying '{noun}'.")
    game["player"]["inventory"].remove(noun)
    room["items"].append(noun)
    return ("response", f"You drop the {noun}.")


def cmd_inventory(noun, game):
    """List what the player is carrying."""
    inv = game["player"]["inventory"]
    if not inv:
        return ("response", "You are empty-handed.")
    lines = "\n".join(f"  • {item}" for item in inv)
    return ("response", f"You are carrying:\n{lines}")


def cmd_attack(noun, game):
    """Attack the living enemy in the current room."""
    enemy, eid = ge.get_enemy_in_room(game)
    if enemy is None:
        return ("error", "There's nothing to fight here.")

    player_dmg = 20
    enemy["health"] -= player_dmg
    game["player"]["health"] -= enemy["damage"]

    if game["player"]["health"] <= 0:
        return ("error",
                f"The {enemy['name']} delivers a fatal blow.\n\n"
                "💀 You have died. Type 'restart' to begin again.")

    if enemy["health"] <= 0:
        enemy["alive"] = False
        game["player"]["score"] += 10
        if eid == "sea_dragon":
            room = ge.get_room(game)
            room["items"].append("key")
            return ("response",
                    "You strike the Sea Dragon one final time! "
                    "It lets out a thunderous roar and collapses into the waves. +10 score.\n\n"
                    "As the beast sinks, an ornate iron key rises to the surface.")
        return ("response",
                f"You strike the {enemy['name']} hard — it collapses. "
                f"-{enemy['damage']} HP. +10 score.\n\nThe way forward is now clear.")

    p = game["player"]
    hint = ""
    if eid == "sea_dragon":
        if "elixir" in game["player"]["inventory"]:
            hint = "\n\nThe elixir pulses in your pack. Type 'drink elixir' before the next blow kills you."
        elif p["health"] <= enemy["damage"]:
            hint = "\n\n⚠ The Sea Dragon's next strike will be fatal."

    return ("response",
            f"You hit the {enemy['name']} for {player_dmg} dmg "
            f"({enemy['health']} HP left).\n"
            f"It hits back for {enemy['damage']} dmg. "
            f"Your HP: {p['health']}/{p['max_health']}."
            + hint)


def cmd_wait(noun, game):
    """Rest and recover a little health."""
    p = game["player"]
    p["health"] = min(p["health"] + 10, p["max_health"])
    return ("response", f"You rest a moment. HP: {p['health']}/{p['max_health']}.")


def cmd_drink(noun, game):
    """Drink the elixir to restore health."""
    if noun is None or noun == "elixir":
        if "elixir" not in game["player"]["inventory"]:
            return ("error", "You don't have an elixir to drink.")
        game["player"]["inventory"].remove("elixir")
        p = game["player"]
        p["health"] = p["max_health"]
        return ("response", f"You drink the elixir. Health restored to {p['health']}/{p['max_health']}. ✨")
    return ("error", f"You can't drink the {noun}.")


def cmd_read(noun, game):
    """Read the parchment."""
    if noun is None:
        return ("error", "Read what? Try: read parchment")

    if noun in ("parchment", "scroll"):
        if "parchment" not in game["player"]["inventory"]:
            return ("error", "You don't have a parchment. Pick one up first.")

        game["player"]["parchment_read"] = True

        return ("response",
                "You unroll the old parchment. The ink is faded but legible:\n\n"
                "  \"I am a bear made of seven stars.\n"
                "   My tail is my brightest point.\n"
                "   Sailors have followed my tail for centuries\n"
                "   to find what they seek.\n"
                "   Which way does my tail point?\"\n\n"
                "Below the riddle, a single word is scratched in different handwriting:\n"
                "  \"THINK.\"\n\n"
                "You fold the parchment away. Something about the night sky "
                "suddenly makes more sense.")

    return ("error", f"You can't read the {noun}.")


def cmd_open(noun, game):
    """Open the chest in the cave with the key."""
    if game["player"]["location"] != "cave":
        return ("error", "There is nothing to open here.")

    room = ge.get_room(game)

    if "lantern" not in game["player"]["inventory"]:
        return ("error", "It's pitch black. You need a lantern.")

    if not room.get("chest_locked", True):
        return ("response", "The chest is already open.")

    if "key" not in game["player"]["inventory"]:
        return ("error",
                "The chest is sealed with an ancient lock. "
                "You need a key to open it.")

    game["player"]["inventory"].remove("key")
    room["chest_locked"] = False
    room["items"].append("grimoire")
    game["player"]["score"] += 50

    return ("response",
            "You slide the key into the lock. It turns with a deep, resonant click.\n\n"
            "The chest swings open. Inside, resting on black silk, sits a grimoire — "
            "bound in midnight leather, its cover etched with constellations that slowly shift. "
            "It hums with quiet knowledge.\n\n"
            "Pick it up to claim your reward. +50 score.")


def cmd_examine(noun, game):
    """Examine an item in inventory or the current room."""
    if noun is None:
        return ("error", "Examine what?")
    target = noun.lower()
    if target in game["items"]:
        room = ge.get_room(game)
        if target in game["player"]["inventory"] or target in room.get("items", []):
            return ("response", game["items"][target]["description"])
    return ("error", f"You don't see any '{noun}' here.")


def cmd_diagnose(noun, game):
    """Check your health and stats."""
    p = game["player"]
    pct = p["health"] / p["max_health"]
    condition = "You feel strong." if pct > 0.7 else "You are wounded." if pct > 0.3 else "You are badly hurt."
    return ("response",
            f"HP: {p['health']}/{p['max_health']}  |  "
            f"Score: {p['score']}  |  Moves: {p['moves']}\n{condition}")


# ============================================================
#  TASK 3 — add your funny commands here
#  Copy the pattern: def cmd_yourword(noun, game):
#                        return ("response", "Something funny happens.")
#  Then add it to COMMAND_MAP at the bottom: "yourword": cmd_yourword,
# ============================================================

def cmd_scream(noun, game):
    return ("response", "AAAAAHHH! The sea is unimpressed.")

def cmd_dance(noun, game):
    return ("response", "You bust out your best moves. Worth it.")

def cmd_pray(noun, game):
    return ("response", "You bow your head. A distant rumble. Probably thunder.")

def cmd_eat(noun, game):
    if noun is None:
        return ("error", "Eat what, exactly?")
    return ("response", f"You attempt to eat the {noun}. It does not go well.")

def cmd_hug(noun, game):
    enemy, _ = ge.get_enemy_in_room(game)
    if enemy:
        return ("response", f"You try to hug the {enemy['name']}. It is baffled.")
    return ("response", "You hug yourself. It helps, a little.")

# ↓ add your commands here ↓


# ============================================================
#  DISPATCHER
# ============================================================

COMMAND_MAP = {
    # Movement
    "go":    cmd_go,
    "north": lambda n, g: cmd_go("north", g),
    "south": lambda n, g: cmd_go("south", g),
    "east":  lambda n, g: cmd_go("east",  g),
    "west":  lambda n, g: cmd_go("west",  g),
    "n":     lambda n, g: cmd_go("north", g),
    "s":     lambda n, g: cmd_go("south", g),
    "e":     lambda n, g: cmd_go("east",  g),
    "w":     lambda n, g: cmd_go("west",  g),
    # Observation
    "look":    cmd_look,
    "l":       cmd_look,
    "examine": cmd_examine,
    # Items
    "pick":  cmd_pick,
    "drop":  cmd_drop,
    # Inventory / status
    "inventory": cmd_inventory,
    "i":         cmd_inventory,
    "diagnose":  cmd_diagnose,
    # Combat
    "attack": cmd_attack,
    "fight":  cmd_attack,
    # Use
    "wait":   cmd_wait,
    "z":      cmd_wait,
    "drink":  cmd_drink,
    "read":   cmd_read,
    "open":   cmd_open,
    "unlock": cmd_open,
    # Funny commands
    "scream": cmd_scream,
    "dance":  cmd_dance,
    "pray":   cmd_pray,
    "eat":    cmd_eat,
    "hug":    cmd_hug,
    # ↓ add your commands here ↓
}


def handle_command(raw, game):
    """Parse and dispatch a command. Returns (kind, message) tuple."""
    if not raw or not raw.strip():
        return ("error", "Type a command.")

    verb, noun = parse_command(raw)

    if verb == "restart":
        return ("__restart__", "")

    handler = COMMAND_MAP.get(verb)
    if handler:
        return handler(noun, game)

    return ("error",
            f"I don't know how to '{verb}'. "
            "Try 'look', 'go north', 'pick <item>', 'attack', or check the commands panel →")