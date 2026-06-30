##############################################################
##############################################################
# TEACHER FILE: DO NOT MODIFY
##############################################################
##############################################################

import copy
import base64
import streamlit as st
from pathlib import Path
from game_world import ROOMS, ITEMS, ENEMIES


# ============================================================
#  GAME STATE
# ============================================================

def initialize_game():
    """Set up fresh game state. Called once when the game starts."""
    return {
        "player": {
            "health":     100,
            "max_health": 100,
            "location":   "ocean_beginning",
            "inventory":  [],
            "score":      0,
            "moves":      0,
        },
        "rooms":   copy.deepcopy(ROOMS),
        "items":   copy.deepcopy(ITEMS),
        "enemies": copy.deepcopy(ENEMIES),
        "log":     [("system", "Welcome, adventurer. Type 'look' to begin.")],
    }


def get_room(game):
    """Return the current room dict."""
    return game["rooms"][game["player"]["location"]]


def get_enemy_in_room(game):
    """Return the first living enemy in the current room, or (None, None)."""
    room = get_room(game)
    for eid in room.get("enemies", []):
        enemy = game["enemies"].get(eid)
        if enemy and enemy["alive"]:
            return enemy, eid
    return None, None


def room_is_blocked(game):
    """Return True if a living enemy is blocking movement."""
    enemy, _ = get_enemy_in_room(game)
    return enemy is not None


# ============================================================
#  UI HELPERS
# ============================================================

def image_to_base64(path: str) -> str | None:
    p = Path(path)
    if not p.exists():
        return None
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render_scene_image(room, game):
    """Render scene image — handles multi-state rooms."""
    img_path = room.get("image", "")

    # Cave: three states based on live lantern possession
    if room.get("image_lit"):
        has_light = "lantern" in game["player"]["inventory"]
        if not room.get("chest_locked", True) or "grimoire" in room.get("items", []):
            img_path = room.get("image_open", room.get("image_lit", img_path))
        elif has_light:
            img_path = room["image_lit"]
        # else stays cave_dark

    # ocean_end: swap image when sea dragon is dead
    elif room.get("image_cleared"):
        all_dead = all(
            not game["enemies"].get(eid, {}).get("alive", True)
            for eid in room.get("enemies", [])
        )
        if all_dead:
            img_path = room["image_cleared"]

    b64 = image_to_base64(img_path) if img_path else None
    if b64:
        ext = Path(img_path).suffix.lstrip(".")
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        st.markdown(f"""
        <div class="scene-image-wrap">
            <img src="data:image/{mime};base64,{b64}" alt="scene"/>
            <div class="location-badge">{room['name']}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="scene-image-wrap">
            <div class="scene-image-placeholder">[ {room['name'].upper()} ]</div>
        </div>""", unsafe_allow_html=True)


def render_inventory(game):
    inv = game["player"]["inventory"]
    items_def = game["items"]
    st.markdown('<div class="inv-header">INVENTORY</div>', unsafe_allow_html=True)
    if not inv:
        st.markdown('<div class="inv-empty">— empty —</div>', unsafe_allow_html=True)
    else:
        chips = ""
        for item_key in inv:
            item = items_def.get(item_key, {})
            label = item.get("name", item_key)
            img_path = item.get("image")
            b64 = image_to_base64(img_path) if img_path else None
            if b64:
                ext = Path(img_path).suffix.lstrip(".")
                icon = f'<img src="data:image/{ext};base64,{b64}" alt="{label}"/>'
            else:
                emoji = item.get("emoji", "📦")
                icon = f'<div class="inv-item-emoji">{emoji}</div>'
            chips += f'<div class="inv-item">{icon}<div class="inv-label">{label}</div></div>'
        st.markdown(f'<div class="inv-grid">{chips}</div>', unsafe_allow_html=True)


def render_stats(game):
    p = game["player"]
    pct = p["health"] / p["max_health"] * 100
    color = "#7fbf9e" if pct > 50 else "#c8a96e" if pct > 25 else "#c06b6b"
    danger_class = "danger" if pct < 30 else ""
    st.markdown(f"""
    <div class="stats-strip">
        <div class="stat-row">
            <span class="stat-label">HEALTH</span>
            <span class="stat-val {danger_class}">{p['health']}/{p['max_health']}</span>
        </div>
        <div class="health-bar">
            <div class="health-fill" style="width:{pct}%;background:{color};"></div>
        </div>
        <div class="stat-row">
            <span class="stat-label">SCORE</span>
            <span class="stat-val">{p['score']}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">MOVES</span>
            <span class="stat-val">{p['moves']}</span>
        </div>
    </div>""", unsafe_allow_html=True)


COMMAND_REFERENCE = [
    ("Movement",    ["go north | n", "go south | s", "go east | e", "go west | w"]),
    ("Look",        ["look | l"]),
    ("Items",       ["pick &lt;item&gt;", "drop &lt;item&gt;", "examine &lt;item&gt;", "inventory | i"]),
    ("Combat",      ["attack | fight"]),
    ("Use",         ["drink elixir", "read parchment", "open chest"]),
    ("Other",       ["restart"]),
]


def render_command_reference():
    st.markdown('<div class="cmd-header">COMMANDS</div>', unsafe_allow_html=True)
    for group, cmds in COMMAND_REFERENCE:
        chips = "".join(f'<div class="cmd-chip">{c}</div>' for c in cmds)
        st.markdown(
            f'<div class="cmd-group-title">{group}</div>'
            f'<div class="cmd-list">{chips}</div>',
            unsafe_allow_html=True)