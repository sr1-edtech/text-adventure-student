# ============================================================
#  ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗
#  ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗
#  ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║
#  ██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║
#  ╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝
#   ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝
#
#  YOUR FILE — define your world here
# ============================================================


# ============================================================
#  ROOMS
# ============================================================

ROOMS = {

    # ── SCENE 1 ──
    "ocean_beginning": {
        "name": "The Sea",  # TASK 1: rename this scene
        "description": (
            "You find yourself on a weathered vessel, surrounded by open ocean. "
            "A flag snaps overhead. You do not know how you got here. "
            "A piece of land is visible to the east. "
            "Your journey lies eastward."
        ),
        "image": "images/rooms/ocean_beginning.png",
        "exits": {"east": "treasure_island"},
        "items": [],
        "enemies": [],
    },

    # ── SCENE 2 ──
    "treasure_island": {
        "name": "SCENE 2",  # TASK 1: rename this scene
        "description": (
            "A single patch of land made of sand and one coconut tree. "
            "A chest lays at the foot of the tree. "
            "The open ocean lies to the south."
        ),
        "image": "images/rooms/treasure_island.png",
        "image_cleared": "images/rooms/treasure_island_updated.png",
        "exits": {"south": "ocean_middle", "west": "ocean_beginning"},
        "items": ["lantern", "coin", "parchment", "elixir"],
        "enemies": ["goblin"],
    },

    # ── SCENE 3 ──
    "ocean_middle": {
        "name": "SCENE 3",  # TASK 1: rename this scene
        "description": (
            "It is pitch dark here. All you can see are bright stars in the night sky "
            "forming a certain shape. A parchment with a clue might help you find the way."
        ),
        "image": "images/rooms/ocean_middle.png",
        "exits": {"north": "ocean_end", "south": "treasure_island"},
        "items": [],
        "enemies": [],
    },

    # ── SCENE 4 ──
    "ocean_end": {
        "name": "SCENE 4",  # TASK 1: rename this scene
        "description": (
            "You are in open water. A rocky shore is visible to the east."
        ),
        "image": "images/rooms/ocean_end.png",
        "image_cleared": "images/rooms/ocean_end_updated.png",
        "exits": {"east": "cave_entrance", "south": "ocean_middle"},
        "items": [],
        "enemies": ["sea_dragon"],
    },

    # ── SCENE 5 ──
    "cave_entrance": {
        "name": "SCENE 5",  # TASK 1: rename this scene
        "description": (
            "You stand on a rocky shore at the base of a cliff. "
            "A cave entrance is carved into the rock to the north. "
            "The open sea lies to the west."
        ),
        "image": "images/rooms/cave_entrance.png",
        "exits": {"north": "cave", "west": "ocean_end"},
        "items": [],
        "enemies": [],
    },

    # ── SCENE 6 ──
    "cave": {
        "name": "SCENE 6",  # TASK 1: rename this scene
        "description": (
            "The cave is pitch black. You can barely see your hand in front of your face. "
            "You sense something extraordinary is in here — but you need light to find it."
        ),
        "description_lit": (
            "Your lantern reveals a breathtaking sight: mountains of gold coins, "
            "strings of pearls, gemstones scattered like fallen stars. "
            "At the centre of it all sits a great iron chest, sealed with an ancient lock."
        ),
        "description_open": (
            "The chest stands open. Inside, resting on a bed of black silk, "
            "sits a grimoire — bound in midnight leather, "
            "its cover etched with constellations that slowly shift and move. "
            "It hums with the quiet knowledge of centuries. "
            "You have reached the end of your journey."
        ),
        "image": "images/rooms/cave_dark.png",
        "image_lit":  "images/rooms/cave_lit.png",
        "image_open": "images/rooms/cave_open.png",
        "exits": {"south": "cave_entrance"},
        "items": [],
        "enemies": [],
        "chest_locked": True,
    },

    # TASK 5 (optional): add your new room here — copy the template below
    # "my_room": {
    #     "name": "My Room",
    #     "description": "Describe what the player sees when they look around.",
    #     "image": None,
    #     "exits": {"west": "cave_entrance"},  # connect back to an existing room
    #     "items": [],
    #     "enemies": [],
    # },

}


# ============================================================
#  ITEMS
# ============================================================

ITEMS = {
    "lantern": {
        "name": "lantern",
        "description": "A battered brass lantern. It still has oil. It will light dark places.",
        "takeable": True,
        "emoji": "🔦",
        "image": "images/items/brass_lantern.png",
    },
    "coin": {
        "name": "coin",
        "description": "A gold coin stamped with an unfamiliar face.",
        "takeable": True,
        "emoji": "🪙",
        "image": "images/items/gold_coin.png",
    },
    "parchment": {
        "name": "parchment",
        "description": (
            "A rolled piece of aged parchment sealed with wax. "
            "Something is written inside. Type 'read parchment' to study it."
        ),
        "takeable": True,
        "emoji": "📜",
        "image": "images/items/treasure_map.png",
    },
    "elixir": {
        "name": "elixir",
        "description": (
            "A shimmering vial of crimson liquid. Drinking it restores full health. "
            "You will need this to survive the Sea Dragon — drink it mid-fight."
        ),
        "takeable": True,
        "emoji": "🧪",
        "image": None,
    },
    "gold": {
        "name": "gold",
        "description": "A heavy pouch overflowing with gold coins. Worth a small fortune.",
        "takeable": True,
        "emoji": "💰",
        "image": None,
    },
    "ruby": {
        "name": "ruby",
        "description": "A flawless ruby the size of your fist, glowing with a deep crimson fire.",
        "takeable": True,
        "emoji": "💎",
        "image": None,
    },
    "sapphire": {
        "name": "sapphire",
        "description": "An enormous sapphire, cool to the touch, blue as the ocean you crossed.",
        "takeable": True,
        "emoji": "🔷",
        "image": None,
    },
    "key": {
        "name": "key",
        "description": (
            "An ornate iron key, slick and warm. The Sea Dragon carried this. "
            "It must unlock something important."
        ),
        "takeable": True,
        "emoji": "🗝️",
        "image": None,
    },
    "grimoire": {
        "name": "grimoire",
        "description": (
            "The Grimoire of Wisdom — bound in midnight leather, its cover etched with "
            "constellations that slowly shift as you watch. You open it. "
            "The first page reads: 'Python Programming: From Zero to Adventure'. "
            "You turn the page. Another chapter appears, unwritten moments ago. "
            "It will never run out of pages. It already knows what you need to learn next."
        ),
        "takeable": True,
        "emoji": "📖",
        "image": None,
    },

    # TASK 4: add your new item here — copy the template below
    # "my_item": {
    #     "name": "my item",
    #     "description": "Write what the player sees when they type 'examine my item'.",
    #     "takeable": True,
    #     "emoji": "⭐",
    #     "image": None,
    # },
    # Then add "my_item" to the "items" list of whichever room you want it to appear in.

}


# ============================================================
#  ENEMIES
# ============================================================

ENEMIES = {
    # TASK 2: change health and damage to make the goblin easier or harder
    # TASK 6 (optional): rename the goblin to a new enemy
    "goblin": {
        "name": "Goblin",          # TASK 6: rename your enemy
        "health": 2000,              # TASK 2: change this number
        "damage": 55,              # TASK 2: change this number
        "alive": True,
        "description": "A scraggly goblin eyes you hungrily, teeth bared.",  # TASK 6: update this
        "dialogue": [
            "Hold it! This treasure belongs to me.",
            "You look lost. The sea tends to have that effect on people.",
            "Last warning: leave the chest alone, or prepare to fight!",
        ],
        "tickle_response": "Knock it off! Goblins are fearsome, not ticklish!",
    },

    # do not change the sea dragon
    "sea_dragon": {
        "name": "Sea Dragon",
        "health": 60,
        "damage": 34,
        "alive": True,
        "description": "A colossal sea dragon rises from the deep, scales like black mirrors.",
        "dialogue": [
            "Mortal, you have sailed far beyond the safety of your kind.",
            "The key you seek was claimed by the sea long ago.",
            "Turn back now. My next words will be spoken in flame.",
        ],
        "tickle_response": "Stop that, tiny mortal! You are testing my patience!",
    },
}
