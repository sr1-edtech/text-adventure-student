##############################################################
##############################################################
# TEACHER FILE: DO NOT MODIFY
##############################################################
##############################################################

import streamlit as st
import streamlit.components.v1 as components
import game_engine as ge
import game_commands as gc

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Text Adventure",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0.25rem 0.5rem 1rem !important; max-width: 100% !important; }

:root {
    --bg:          #0e0e10;
    --panel:       #0a0a0c;
    --surface:     #1a1a1e;
    --surface-2:   #222228;
    --surface-3:   #16161a;
    --border:      #2a2a32;
    --border-soft: #1e1e24;
    --text-primary:   #e2e2e8;
    --text-secondary: #9090a8;
    --text-muted:     #50506a;
    --accent:      #c8a96e;
    --accent-dim:  #7a6440;
    --positive:    #7fbf9e;
    --negative:    #c06b6b;
    --alert:       #d4843a;
    --font-ui:     'Inter', system-ui, sans-serif;
    --font-mono:   'JetBrains Mono', 'Courier New', monospace;
}

div[data-testid="stAppViewContainer"] { background: var(--bg); }

/* tighten gap between columns */
div[data-testid="stHorizontalBlock"] { gap: 0 !important; }
div[data-testid="stHorizontalBlock"] > div:last-child { padding-left: 0.75rem !important; }

/* ── SCENE IMAGE ── */
.scene-image-wrap {
    width: 100%; height: 0; padding-bottom: 50%;
    overflow: hidden; position: relative;
    border: 1px solid var(--border); border-radius: 4px;
    margin-bottom: 16px;
}
.scene-image-wrap img {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    object-fit: cover; display: block; filter: brightness(0.75) saturate(0.8);
}
.scene-image-placeholder {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: var(--surface); display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted);
    letter-spacing: 0.25em; text-transform: uppercase;
}
.location-badge {
    position: absolute; bottom: 0; left: 0; right: 0; padding: 36px 16px 12px;
    background: linear-gradient(transparent, rgba(10,10,12,0.96));
    font-family: var(--font-ui); font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.16em; text-transform: uppercase; color: var(--accent);
}

/* ── INPUT ── */
div[data-testid="stTextInput"] > div > div > input {
    background: var(--surface-3) !important; border: 1px solid var(--border) !important;
    border-radius: 4px !important; color: var(--text-primary) !important;
    font-family: var(--font-mono) !important; font-size: 0.82rem !important;
    caret-color: var(--accent) !important; padding: 8px 12px !important; box-shadow: none !important;
}
div[data-testid="stTextInput"] > div > div > input::placeholder { color: var(--text-muted) !important; }
div[data-testid="stTextInput"] > div > div > input:focus { border-color: var(--accent-dim) !important; box-shadow: none !important; }
div[data-testid="stTextInput"] label { display: none !important; }

/* ── LOG ENTRIES ── */
.log-entry { font-family: var(--font-mono); font-size: 0.82rem; line-height: 1.7; padding: 5px 0; border-bottom: 1px solid var(--border-soft); color: var(--text-primary); }
.log-entry.cmd      { color: var(--text-muted); font-size: 0.74rem; }
.log-entry.response { color: var(--positive); }
.log-entry.error    { color: var(--negative); }
.log-entry.system   { color: var(--text-secondary); font-style: italic; font-size: 0.74rem; }
.log-entry.alert    { color: var(--alert); }

/* ── RIGHT PANEL — one long sidebar ── */
div[data-testid="stHorizontalBlock"] > div:last-child > div {
    background: var(--panel); border-left: 1px solid var(--border); padding: 0 0.5rem; min-height: 100vh;
}
.inv-header { font-family: var(--font-ui); font-size: 0.62rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); padding: 14px 0 8px; border-bottom: 1px solid var(--border); margin-bottom: 8px; }
.cmd-header { font-family: var(--font-ui); font-size: 0.62rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--text-secondary); padding: 8px 0; margin-top: 8px; border-top: 2px solid var(--border); border-bottom: 1px solid var(--border); margin-bottom: 8px; }
.inv-grid { display: flex; flex-wrap: wrap; gap: 6px; padding: 4px 0 12px; min-height: 60px; }
.inv-item { display: flex; flex-direction: column; align-items: center; gap: 3px; background: var(--surface); border: 1px solid var(--border); border-radius: 3px; padding: 7px 8px 5px; width: 60px; }
.inv-item-emoji { font-size: 1.3rem; line-height: 1; }
.inv-item img { width: 30px; height: 30px; object-fit: contain; opacity: 0.85; }
.inv-label { font-family: var(--font-mono); font-size: 0.54rem; color: var(--text-secondary); text-align: center; word-break: break-word; }
.inv-empty { font-family: var(--font-mono); font-size: 0.68rem; color: var(--text-secondary); font-style: italic; padding: 4px 0; }
.stats-strip { display: flex; flex-direction: column; gap: 7px; padding: 10px 0 4px; border-top: 1px solid var(--border); }
.stat-row { font-family: var(--font-mono); font-size: 0.7rem; display: flex; justify-content: space-between; align-items: center; }
.stat-label { color: var(--accent); letter-spacing: 0.1em; font-size: 0.6rem; text-transform: uppercase; font-family: var(--font-ui); font-weight: 600; }
.stat-val { color: var(--text-primary); font-weight: 500; }
.stat-val.danger { color: var(--negative); }
.health-bar { height: 3px; background: var(--surface-2); border-radius: 2px; overflow: hidden; margin-top: 2px; }
.health-fill { height: 100%; border-radius: 2px; transition: width 0.4s ease; }

/* ── COMMAND REFERENCE ── */
.cmd-group-title { font-family: var(--font-ui); font-size: 0.58rem; font-weight: 600; color: var(--text-secondary); letter-spacing: 0.14em; text-transform: uppercase; padding: 6px 0 5px; border-bottom: 1px solid var(--border-soft); margin-bottom: 5px; }
.cmd-list { display: flex; flex-direction: column; gap: 5px; padding-bottom: 6px; }
.cmd-chip { font-family: var(--font-mono); font-size: 0.64rem; color: var(--text-primary); background: var(--surface); border: 1px solid var(--border); border-radius: 3px; padding: 4px 8px; display: inline-block; }

/* ── MOBILE STATUS BAR — hidden on desktop, shown on mobile ── */
.mob-status { display: none; }

/* ── MOBILE / TABLET HAMBURGER ── */
.mob-hamburger, .mob-panel, .mob-overlay { display: none; }

@media (max-width: 1024px) {
    .scene-image-wrap { padding-bottom: 75% !important; }

    /* hide desktop right panel */
    div[data-testid="stHorizontalBlock"] > div:last-child { display: none !important; }

    /* inline status bar */
    .mob-status {
        display: block;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 10px 14px;
        margin: 8px 0;
    }
    .mob-status-row {
        display: flex; align-items: center; gap: 10px;
        padding: 7px 0; border-bottom: 1px solid var(--border-soft);
        font-family: var(--font-mono); font-size: 0.78rem;
    }
    .mob-status-row:last-child { border-bottom: none; padding-bottom: 0; }
    .mob-status-label {
        font-family: var(--font-ui); font-size: 0.58rem; font-weight: 600;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: var(--accent); min-width: 76px; flex-shrink: 0;
    }
    .mob-status-val { color: var(--text-primary); }
    .mob-status-val.danger { color: var(--negative); }
    .mob-inv-chips { display: flex; gap: 6px; flex-wrap: wrap; }
    .mob-inv-chip { background: var(--surface); border: 1px solid var(--border); border-radius: 3px; padding: 2px 8px; font-size: 0.72rem; color: var(--text-primary); }
    .mob-inv-empty { color: var(--text-muted); font-style: italic; font-size: 0.72rem; }
    .mob-hbar { flex: 1; height: 3px; background: var(--surface-2); border-radius: 2px; overflow: hidden; margin-left: 8px; }
    .mob-hfill { height: 100%; border-radius: 2px; }
    .mob-half { flex: 1; display: flex; align-items: center; gap: 8px; }

    /* hamburger — commands only */
    .mob-hamburger {
        display: block; position: fixed; top: 10px; right: 12px; z-index: 1000;
        background: var(--surface); border: 1px solid var(--border); border-radius: 4px;
        color: var(--accent); font-size: 1.2rem; padding: 4px 11px; cursor: pointer; line-height: 1.4;
    }
    .mob-panel {
        display: block; position: fixed; top: 0; right: 0;
        width: 86vw; max-width: 340px; height: 100vh;
        background: var(--panel); border-left: 1px solid var(--border);
        z-index: 999; overflow-y: auto; padding: 48px 14px 24px;
        transform: translateX(100%); transition: transform 0.22s ease;
    }
    .mob-panel.open { transform: translateX(0); }
    .mob-overlay { display: none; position: fixed; inset: 0; z-index: 998; background: rgba(0,0,0,0.5); }
    .mob-overlay.open { display: block; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# MAIN BODY
# ============================================================

if "game" not in st.session_state:
    st.session_state.game = ge.initialize_game()
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

game = st.session_state.game

left, right = st.columns([3, 1], gap="small")

with left:
    ge.render_scene_image(ge.get_room(game), game)

    raw = st.text_input(
        "command",
        key=f"cmd_{st.session_state.input_key}",
        placeholder="❯  type a command...",
        label_visibility="collapsed",
        autocomplete="off",
    )

    if raw:
        result = gc.handle_command(raw, game)
        if result[0] == "__restart__":
            st.session_state.game = ge.initialize_game()
            st.session_state.input_key += 1
            st.rerun()
        else:
            game["log"].append(("cmd", f"❯ {raw}"))
            game["log"].append(result)
            st.session_state.input_key += 1
            st.rerun()

    # ── MOBILE STATUS BAR — rendered by Python every rerun, always fresh ──
    p = game["player"]
    inv = game["player"]["inventory"]
    items_def = game["items"]
    pct = p["health"] / p["max_health"] * 100
    hcolor = "#7fbf9e" if pct > 50 else "#c8a96e" if pct > 25 else "#c06b6b"
    danger = "danger" if pct < 30 else ""
    inv_html = "".join(
        f'<span class="mob-inv-chip">{items_def.get(k,{}).get("emoji","📦")} {items_def.get(k,{}).get("name",k)}</span>'
        for k in inv
    ) if inv else '<span class="mob-inv-empty">— empty —</span>'

    st.markdown(f"""<div class="mob-status">
    <div class="mob-status-row">
        <span class="mob-status-label">Inventory</span>
        <div class="mob-inv-chips">{inv_html}</div>
    </div>
    <div class="mob-status-row">
        <span class="mob-status-label">Health</span>
        <span class="mob-status-val {danger}">{p['health']}/{p['max_health']}</span>
        <div class="mob-hbar"><div class="mob-hfill" style="width:{pct}%;background:{hcolor};"></div></div>
    </div>
    <div class="mob-status-row">
        <div class="mob-half"><span class="mob-status-label">Score</span><span class="mob-status-val">{p['score']}</span></div>
        <div class="mob-half"><span class="mob-status-label">Moves</span><span class="mob-status-val">{p['moves']}</span></div>
    </div>
</div>""", unsafe_allow_html=True)

    log = game["log"]

    def render_entry(kind, msg):
        safe = msg.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        if safe.startswith("[ALERT]"):
            safe = safe.replace("[ALERT]", "⚠", 1)
            st.markdown(f'<div class="log-entry alert">{safe}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="log-entry {kind}">{safe}</div>', unsafe_allow_html=True)

    i = len(log) - 1
    while i >= 0:
        if i > 0 and log[i - 1][0] == "cmd":
            render_entry(*log[i - 1])
            render_entry(*log[i])
            i -= 2
        else:
            render_entry(*log[i])
            i -= 1

with right:
    ge.render_inventory(game)
    ge.render_stats(game)
    ge.render_command_reference()

# ============================================================
# JS — ONE IFRAME ONLY, AT THE BOTTOM
# ============================================================

components.html("""
<script>
(function() {
    const doc = window.parent.document;

    function focusInput() {
        const inputs = doc.querySelectorAll('input[type="text"]');
        inputs.forEach(inp => {
            inp.setAttribute("autocomplete", "off");
            inp.setAttribute("autocorrect", "off");
            inp.setAttribute("autocapitalize", "none");
            inp.setAttribute("spellcheck", "false");
        });
        if (inputs.length > 0) inputs[0].focus();
    }

    function ensureMobilePanel() {
        // Always remove and re-create so event listeners survive Streamlit reruns
        var oldBtn = doc.getElementById("mob-hamburger");
        if (oldBtn) oldBtn.remove();
        var oldOverlay = doc.getElementById("mob-overlay");
        if (oldOverlay) oldOverlay.remove();
        var oldPanel = doc.getElementById("mob-panel");
        var panelWasOpen = oldPanel && oldPanel.classList.contains("open");
        if (oldPanel) oldPanel.remove();

        const btn = doc.createElement("button");
        btn.id = "mob-hamburger"; btn.className = "mob-hamburger";
        btn.textContent = panelWasOpen ? "✕" : "☰";
        doc.body.appendChild(btn);

        const overlay = doc.createElement("div");
        overlay.id = "mob-overlay"; overlay.className = "mob-overlay";
        if (panelWasOpen) overlay.classList.add("open");
        doc.body.appendChild(overlay);

        const panel = doc.createElement("div");
        panel.id = "mob-panel"; panel.className = "mob-panel";
        if (panelWasOpen) panel.classList.add("open");
        doc.body.appendChild(panel);

        function closePanel() { panel.classList.remove("open"); overlay.classList.remove("open"); btn.textContent = "☰"; }
        function openPanel()  { panel.classList.add("open");    overlay.classList.add("open");    btn.textContent = "✕"; }

        btn.addEventListener("click", function() { panel.classList.contains("open") ? closePanel() : openPanel(); });
        overlay.addEventListener("click", closePanel);

        // Copy full right panel, hide inv/stats by class
        const rightCol = doc.querySelector('div[data-testid="stHorizontalBlock"] > div:last-child > div');
        if (panel && rightCol) {
            panel.innerHTML = rightCol.innerHTML;
            ['.inv-header','.inv-grid','.inv-empty','.stats-strip','.inv-item'].forEach(function(sel) {
                panel.querySelectorAll(sel).forEach(function(el) { el.style.display = 'none'; });
            });
        }
    }

    setTimeout(focusInput, 50);
    setTimeout(focusInput, 200);
    setTimeout(focusInput, 500);
    setTimeout(ensureMobilePanel, 500);
    setTimeout(ensureMobilePanel, 1000);
    setTimeout(ensureMobilePanel, 2000);
})();
</script>
""", height=0)