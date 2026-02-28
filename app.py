import streamlit as st
import random
import io
import time
import math

# ─── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="🎉 Bingo Builder for Kids",
    page_icon="🎱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

TEMPLATES = {
    "Numbers 1-20":  [str(i) for i in range(1, 21)],
    "Numbers 1-50":  [str(i) for i in range(1, 51)],
    "Colors":        ["Red","Blue","Green","Yellow","Orange","Purple","Pink","Brown",
                      "Black","White","Gray","Cyan","Lime","Indigo","Violet",
                      "Gold","Silver","Teal","Coral","Salmon","Peach","Mint",
                      "Lavender","Crimson","Sky Blue"],
    "Basic Vocab":   ["Apple","Ball","Cat","Dog","Egg","Fish","Girl","Hat","Ice","Jump",
                      "King","Lamp","Moon","Nest","Open","Play","Queen","Rain","Sun","Tree",
                      "Under","Van","Wind","Box","Year","Zoo","Ant","Bee","Cup","Door"],
}

CELL_PALETTE = [
    "#FF6B6B","#FF9F43","#FFEAA7","#A8E6CF","#81ECEC",
    "#74B9FF","#A29BFE","#FD79A8","#FDCB6E","#55EFC4",
    "#E17055","#0984E3","#6C5CE7","#00CEC9","#E84393",
]

# Each call gets a unique gradient from this set — rotated per call index
CALLER_GRADIENTS = [
    ("135deg", "#FF6B6B", "#FF9F43", "#FFEAA7"),
    ("135deg", "#4d96ff", "#6bcb77", "#FFEAA7"),
    ("135deg", "#c77dff", "#4d96ff", "#81ECEC"),
    ("135deg", "#FD79A8", "#FDCB6E", "#FF6B6B"),
    ("135deg", "#55EFC4", "#74B9FF", "#A29BFE"),
    ("135deg", "#6bcb77", "#FFEAA7", "#FD79A8"),
    ("135deg", "#E84393", "#c77dff", "#74B9FF"),
    ("135deg", "#FF9F43", "#55EFC4", "#4d96ff"),
]

CONFETTI_COLORS = [
    "#FF6B6B","#FF9F43","#FFEAA7","#6bcb77","#4d96ff",
    "#c77dff","#FD79A8","#55EFC4","#E84393","#FDCB6E",
]

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS — all animations live here
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Fonts ──────────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Fredoka+One&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

/* ── App background (animated) ──────────────────────────────────────────── */
@keyframes appBgDrift {
    0%   { background-position: 0% 0%; }
    50%  { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}
.main {
    background: linear-gradient(135deg, #f0f4ff 0%, #fff0fb 40%, #f0fff8 80%, #f7f0ff 100%);
    background-size: 300% 300%;
    animation: appBgDrift 20s ease infinite;
}

/* ── App title ──────────────────────────────────────────────────────────── */
@keyframes titleFloat {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}
.app-title {
    text-align: center;
    font-family: 'Fredoka One', cursive;
    font-size: 3rem;
    background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff, #c77dff, #ff6b6b);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleFloat 3s ease-in-out infinite, titleColorShift 4s linear infinite;
    margin-bottom: 0;
    filter: drop-shadow(0 2px 8px rgba(92,53,217,0.2));
}
@keyframes titleColorShift {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}
.app-sub { text-align:center; color:#888; font-size:1.05rem; margin-top:4px; }

/* ── Tabs ───────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap:10px; background:#e8e0ff; border-radius:18px; padding:6px;
}
.stTabs [data-baseweb="tab"] {
    background:white; border-radius:14px; font-weight:700;
    font-size:1.05rem; color:#5c35d9; padding:10px 28px;
    transition: all 0.25s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    background: #f0ebff; transform: translateY(-1px);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#5c35d9,#9b59b6) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(92,53,217,0.35);
}

/* ── Bingo card preview ─────────────────────────────────────────────────── */
.bingo-card {
    background:white; border-radius:22px; padding:14px; margin:8px;
    box-shadow:0 6px 20px rgba(92,53,217,0.13); border:3px solid #c9b8ff;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.bingo-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(92,53,217,0.22);
}
.bingo-card-title {
    text-align:center; font-family:'Fredoka One',cursive;
    font-size:1.2rem; color:#5c35d9; margin-bottom:10px; letter-spacing:1px;
}

/* ── Buttons ────────────────────────────────────────────────────────────── */
.stButton > button {
    border-radius:16px; font-weight:700; font-size:1rem;
    padding:10px 24px; border:none; transition: all 0.22s cubic-bezier(.34,1.56,.64,1);
    position: relative; overflow: hidden;
}
.stButton > button:hover {
    transform: scale(1.07) translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.18);
}
.stButton > button:active { transform: scale(0.97); }

/* ── Error box ──────────────────────────────────────────────────────────── */
.error-box {
    background:#ffe0e0; border:2px solid #ffb3b3; border-radius:14px;
    padding:14px 20px; color:#c0392b; font-weight:700; margin:10px 0;
}

/* ── History chips ──────────────────────────────────────────────────────── */
.history-chip {
    display:inline-block; background:#e8e0ff; color:#5c35d9;
    border-radius:22px; padding:5px 14px; margin:3px;
    font-weight:700; font-size:0.88rem;
    transition: transform 0.15s ease;
}
.history-chip:hover { transform: scale(1.08); }


/* ════════════════════════════════════════════════════════════════════════
   PLAY CALLER — MAGIC STAGE
   ════════════════════════════════════════════════════════════════════════ */

/* Outer pulsing border ring */
@keyframes borderPulse {
    0%   { box-shadow: 0 0 0 0 rgba(255,255,255,0.7), 0 12px 50px rgba(0,0,0,0.22); }
    50%  { box-shadow: 0 0 0 14px rgba(255,255,255,0.0), 0 12px 50px rgba(0,0,0,0.22); }
    100% { box-shadow: 0 0 0 0 rgba(255,255,255,0.0), 0 12px 50px rgba(0,0,0,0.22); }
}

/* Stage wrapper */
.caller-stage {
    border-radius: 32px;
    padding: 5px;
    margin: 18px 0;
    animation: borderPulse 2.2s ease-out infinite;
    position: relative;
    overflow: hidden;
}

/* Animated gradient fill */
@keyframes gradientSpin {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.caller-stage-bg {
    position: absolute; inset: 0;
    background-size: 300% 300%;
    animation: gradientSpin 5s ease infinite;
    border-radius: 32px;
    z-index: 0;
}

.caller-inner {
    position: relative; z-index: 1;
    background: rgba(0,0,0,0.08);
    backdrop-filter: blur(2px);
    border-radius: 28px;
    padding: 36px 24px 28px;
    text-align: center;
}

/* Glowing aura behind number */
@keyframes auraBreath {
    0%, 100% { transform: scale(1);   opacity: 0.55; }
    50%       { transform: scale(1.15); opacity: 0.85; }
}
.caller-aura {
    position: absolute;
    left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    width: 220px; height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.65) 0%, rgba(255,255,255,0) 70%);
    animation: auraBreath 2s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

/* Number pop-in */
@keyframes numberPop {
    0%   { transform: scale(0.25) rotate(-12deg); opacity: 0; filter: blur(8px); }
    55%  { transform: scale(1.18)  rotate(4deg);  opacity: 1; filter: blur(0); }
    75%  { transform: scale(0.94)  rotate(-2deg); }
    90%  { transform: scale(1.04)  rotate(1deg); }
    100% { transform: scale(1)     rotate(0deg); opacity: 1; }
}
/* Idle floating */
@keyframes numberFloat {
    0%, 100% { transform: translateY(0px) scale(1); }
    50%       { transform: translateY(-10px) scale(1.02); }
}
.caller-number-wrap {
    position: relative; display: inline-block;
}
.caller-number {
    font-family: 'Fredoka One', cursive;
    font-size: clamp(4rem, 10vw, 8.5rem);
    color: white;
    text-shadow: 0 4px 0 rgba(0,0,0,0.2), 0 8px 30px rgba(0,0,0,0.15);
    line-height: 1.05;
    display: block;
    animation: numberPop 0.65s cubic-bezier(.36,.07,.19,.97) both,
               numberFloat 3s ease-in-out 0.9s infinite;
    position: relative; z-index: 2;
}

/* Sparkle particles — pure CSS */
@keyframes sparkleFly {
    0%   { transform: translate(0,0) scale(1) rotate(0deg);   opacity: 1; }
    100% { transform: translate(var(--tx), var(--ty)) scale(0) rotate(var(--tr)); opacity: 0; }
}
.sparkle {
    position: absolute;
    width: 10px; height: 10px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 3;
    animation: sparkleFly var(--dur) ease-out var(--delay) both;
}

/* Called label */
@keyframes labelBounce {
    0%, 100% { transform: translateY(0)    scale(1); }
    25%       { transform: translateY(-8px) scale(1.05); }
    60%       { transform: translateY(-3px) scale(0.98); }
}
.caller-label {
    font-size: 1.25rem; color: rgba(255,255,255,0.95); font-weight:800;
    letter-spacing: 2px; margin-top: 10px;
    animation: labelBounce 1.4s ease 0.7s 3;
    display: inline-block;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

/* Idle state */
@keyframes idlePulse {
    0%, 100% { opacity: 0.55; transform: scale(1); }
    50%       { opacity: 0.85; transform: scale(1.03); }
}
.caller-idle {
    font-family: 'Fredoka One', cursive;
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    color: rgba(255,255,255,0.7);
    padding: 50px 0;
    animation: idlePulse 2.5s ease-in-out infinite;
}

/* Progress bar */
.progress-wrap {
    background: rgba(255,255,255,0.25); border-radius:20px;
    height: 16px; margin: 18px 0 6px; overflow:hidden;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}
@keyframes progressShimmer {
    0%   { background-position: -200px 0; }
    100% { background-position: 200px 0; }
}
.progress-fill {
    height: 100%; border-radius:20px;
    background: linear-gradient(90deg,
        rgba(255,255,255,0.5) 0%,
        rgba(255,255,255,0.9) 40%,
        rgba(255,255,255,0.6) 60%,
        rgba(255,255,255,0.5) 100%);
    background-size: 200px 100%;
    animation: progressShimmer 1.8s linear infinite;
    transition: width 0.6s cubic-bezier(.34,1.56,.64,1);
}
.progress-label {
    color: rgba(255,255,255,0.9); font-size:1rem; font-weight:800;
    margin-top:6px; text-shadow: 0 1px 4px rgba(0,0,0,0.18);
}

/* Live badge */
@keyframes livePing {
    0%   { transform: scale(1);   opacity:1; }
    70%  { transform: scale(1.4); opacity:0; }
    100% { transform: scale(1);   opacity:0; }
}
.live-badge {
    display: inline-flex; align-items:center; gap:8px;
    background: rgba(255,255,255,0.2); color:white;
    border-radius: 24px; padding: 6px 18px; font-weight:800;
    font-size:0.95rem; border: 2px solid rgba(255,255,255,0.5);
    backdrop-filter: blur(4px);
}
.live-dot {
    width:10px; height:10px; border-radius:50%;
    background: #ff4444;
    position: relative;
}
.live-dot::after {
    content:''; position:absolute; inset:0;
    border-radius:50%; background:#ff4444;
    animation: livePing 1.2s ease-out infinite;
}


/* ════════════════════════════════════════════════════════════════════════
   CONFETTI + WIN CELEBRATION
   ════════════════════════════════════════════════════════════════════════ */

@keyframes confettiFall {
    0%   { transform: translateY(-40px) rotate(0deg)   scaleX(1); opacity: 1; }
    80%  { opacity: 1; }
    100% { transform: translateY(calc(100vh + 20px)) rotate(var(--r)) scaleX(var(--sx)); opacity: 0; }
}
.confetti-piece {
    position: fixed;
    top: -40px;
    left: var(--x);
    width: var(--w);
    height: var(--h);
    background: var(--c);
    border-radius: var(--br);
    animation: confettiFall var(--dur) ease-in var(--delay) both;
    z-index: 9999;
    pointer-events: none;
}

@keyframes winTitlePop {
    0%   { transform: scale(0) rotate(-10deg); opacity:0; }
    60%  { transform: scale(1.15) rotate(3deg); opacity:1; }
    80%  { transform: scale(0.95) rotate(-2deg); }
    100% { transform: scale(1) rotate(0deg); opacity:1; }
}
@keyframes rainbowText {
    0%   { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(360deg); }
}
@keyframes winFloat {
    0%, 100% { transform: translateY(0) scale(1) rotate(-1deg); }
    50%       { transform: translateY(-18px) scale(1.04) rotate(1deg); }
}
@keyframes winSparkleOrbit {
    from { transform: rotate(0deg) translateX(100px) rotate(0deg); }
    to   { transform: rotate(360deg) translateX(100px) rotate(-360deg); }
}

.win-overlay {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(3px);
    z-index: 9990;
    display: flex; align-items:center; justify-content:center;
}
.win-card {
    background: linear-gradient(135deg, #1a0533, #0d1b4b, #0a2e1a);
    border-radius: 36px;
    padding: 52px 60px;
    text-align: center;
    box-shadow: 0 30px 80px rgba(0,0,0,0.5),
                0 0 0 3px rgba(255,255,255,0.15);
    position: relative;
    overflow: hidden;
    max-width: 540px; width: 90%;
    animation: winTitlePop 0.7s cubic-bezier(.36,.07,.19,.97) both;
}
.win-shimmer {
    position: absolute; inset: 0;
    background: linear-gradient(135deg,
        rgba(255,255,255,0.04) 0%,
        rgba(255,255,255,0.10) 50%,
        rgba(255,255,255,0.04) 100%);
    animation: gradientSpin 3s ease infinite;
    background-size: 200% 200%;
}
.win-emoji {
    font-size: 4.5rem;
    animation: winFloat 2s ease-in-out infinite;
    display: block; line-height:1; margin-bottom:8px;
}
.win-title {
    font-family: 'Fredoka One', cursive;
    font-size: clamp(3rem, 8vw, 5.5rem);
    color: #ffd93d;
    text-shadow: 0 0 20px rgba(255,217,61,0.8),
                 0 0 60px rgba(255,217,61,0.4),
                 4px 5px 0 rgba(0,0,0,0.3);
    animation: rainbowText 2s linear infinite,
               winFloat 2.5s ease-in-out 0.3s infinite;
    display: block; margin: 8px 0;
}
.win-subtitle {
    font-size: 1.4rem; color: rgba(255,255,255,0.88);
    font-weight:800; letter-spacing:2px; margin-bottom: 28px;
    animation: winFloat 3s ease-in-out 0.6s infinite;
}

/* Orbiting sparkles around win card */
.win-sparkle {
    position: absolute;
    width: 14px; height: 14px;
    border-radius: 50%;
    top: 50%; left: 50%;
    margin: -7px;
    animation: winSparkleOrbit var(--orb-dur) linear infinite var(--orb-delay);
}

/* Play Again button */
@keyframes btnGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(255,217,61,0.5), 0 6px 20px rgba(0,0,0,0.3); }
    50%       { box-shadow: 0 0 40px rgba(255,217,61,0.9), 0 6px 20px rgba(0,0,0,0.3); }
}
.win-btn {
    display: inline-block;
    background: linear-gradient(135deg, #ffd93d, #ff9f43);
    color: #1a0533;
    font-family: 'Fredoka One', cursive;
    font-size: 1.6rem;
    padding: 16px 48px;
    border-radius: 50px;
    border: none;
    cursor: pointer;
    font-weight:900;
    text-decoration: none;
    animation: btnGlow 1.8s ease-in-out infinite;
    transition: transform 0.2s cubic-bezier(.34,1.56,.64,1);
    letter-spacing: 1px;
}
.win-btn:hover { transform: scale(1.08) translateY(-3px); }

</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
_defaults = {
    "cards": None,
    "grid_size": 5,
    "items": [],
    "words_input": "",
    "error_msg": None,
    "caller_pool": [],
    "caller_history": [],
    "caller_current": None,
    "caller_call_count": 0,       # increments each call — drives gradient rotation
    "caller_mode": "manual",
    "auto_running": False,
    "auto_last_tick": 0.0,
    "auto_interval": 3,
    "show_win": False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def fisher_yates_shuffle(lst):
    arr = list(lst)
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def generate_cards(items, grid_size, num_cards, free_space):
    total_cells = grid_size * grid_size
    needed = total_cells - (1 if free_space else 0)
    if len(items) < needed:
        return None, (
            f"Not enough items! You need at least **{needed}** unique items "
            f"for a {grid_size}×{grid_size} grid (you have {len(items)})."
        )
    free_pos = (grid_size // 2) * grid_size + (grid_size // 2) if free_space else -1
    cards = []
    for _ in range(num_cards):
        shuffled = fisher_yates_shuffle(items)[:needed]
        card, item_idx = [], 0
        for cell in range(total_cells):
            if cell == free_pos:
                card.append("FREE")
            else:
                card.append(shuffled[item_idx])
                item_idx += 1
        cards.append(card)
    return cards, None


def pick_gradient(call_count):
    """Return CSS gradient string, rotating through CALLER_GRADIENTS."""
    g = CALLER_GRADIENTS[call_count % len(CALLER_GRADIENTS)]
    return f"linear-gradient({g[0]}, {g[1]}, {g[2]}, {g[3]})"


# ══════════════════════════════════════════════════════════════════════════════
#  HTML BUILDERS — caller display, confetti, win screen
# ══════════════════════════════════════════════════════════════════════════════

def _sparkles_html(n=12, spread=140):
    """Generate n CSS sparkle dots radiating from center."""
    parts = []
    colors_spark = ["#fff", "#ffd93d", "#ff6b6b", "#6bcb77", "#4d96ff", "#c77dff", "#FD79A8"]
    for i in range(n):
        angle = (360 / n) * i
        dist  = random.randint(spread // 2, spread)
        tx    = int(dist * math.cos(math.radians(angle)))
        ty    = int(dist * math.sin(math.radians(angle)))
        color = random.choice(colors_spark)
        size  = random.randint(6, 14)
        dur   = round(random.uniform(0.5, 0.9), 2)
        delay = round(random.uniform(0.0, 0.3), 2)
        rot   = random.randint(-180, 180)
        parts.append(
            f'<div class="sparkle" style="'
            f'--tx:{tx}px;--ty:{ty}px;--tr:{rot}deg;'
            f'--dur:{dur}s;--delay:{delay}s;'
            f'background:{color};width:{size}px;height:{size}px;'
            f'left:calc(50% - {size//2}px);top:calc(50% - {size//2}px);'
            f'"></div>'
        )
    return "".join(parts)


def caller_display_html(current, pct, called, total, call_count):
    """Full magic stage HTML for the caller display."""
    gradient = pick_gradient(call_count)
    sparkles = _sparkles_html(16, 130) if current else ""

    if current:
        content = f"""
        <div class="caller-aura"></div>
        <div class="caller-number-wrap">
            {sparkles}
            <span class="caller-number">{current}</span>
        </div>
        <div class="caller-label">✨ &nbsp; Called! &nbsp; ✨</div>
        <div class="progress-wrap">
            <div class="progress-fill" style="width:{pct}%;"></div>
        </div>
        <div class="progress-label">{called} of {total} called</div>
        """
    else:
        content = '<div class="caller-idle">🎱 Press ▶ to start calling!</div>'

    return f"""
    <div class="caller-stage">
        <div class="caller-stage-bg" style="background:{gradient};"></div>
        <div class="caller-inner">
            {content}
        </div>
    </div>
    """


def confetti_html(n=80):
    """CSS-only falling confetti. Lightweight, no JS."""
    pieces = []
    shapes = ["50%", "2px", "4px", "0"]  # circle, thin rect, rect, square
    for i in range(n):
        color  = random.choice(CONFETTI_COLORS)
        x      = random.randint(0, 100)
        w      = random.randint(8, 16)
        h      = random.randint(10, 22)
        dur    = round(random.uniform(1.8, 4.0), 2)
        delay  = round(random.uniform(0.0, 2.5), 2)
        rot    = random.randint(-360, 360)
        sx     = round(random.uniform(0.4, 1.0), 2)
        br     = random.choice(shapes)
        pieces.append(
            f'<div class="confetti-piece" style="'
            f'--x:{x}vw;--w:{w}px;--h:{h}px;--c:{color};--br:{br};'
            f'--dur:{dur}s;--delay:{delay}s;--r:{rot}deg;--sx:{sx};'
            f'"></div>'
        )
    return "".join(pieces)


def win_screen_html():
    """Full win celebration overlay — confetti + trophy card."""
    sparkle_orbs = []
    orb_colors = ["#ffd93d","#ff6b6b","#6bcb77","#4d96ff","#c77dff","#FD79A8"]
    for i in range(6):
        c     = orb_colors[i % len(orb_colors)]
        dur   = round(2.5 + i * 0.5, 1)
        delay = round(i * 0.4, 1)
        sparkle_orbs.append(
            f'<div class="win-sparkle" style="background:{c};'
            f'--orb-dur:{dur}s;--orb-delay:{delay}s;"></div>'
        )
    orbs_html = "".join(sparkle_orbs)

    return f"""
    {confetti_html(90)}
    <div class="win-overlay">
        <div class="win-card">
            <div class="win-shimmer"></div>
            {orbs_html}
            <span class="win-emoji">🏆</span>
            <span class="win-title">BINGO!</span>
            <div class="win-subtitle">🎉 All items called! 🎉</div>
            <form action="" method="get">
                <button class="win-btn" name="play_again" value="1" type="submit">
                    🎮 Play Again
                </button>
            </form>
        </div>
    </div>
    """


# ══════════════════════════════════════════════════════════════════════════════
#  CARD HTML PREVIEW
# ══════════════════════════════════════════════════════════════════════════════

def render_card_html(card, grid_size, card_num, bw_mode):
    cell_size = max(42, min(82, 300 // grid_size))
    font_size = max(0.65, min(1.2, cell_size / 62))
    rows_html = ""
    for r in range(grid_size):
        row_html = "<tr>"
        for c in range(grid_size):
            idx = r * grid_size + c
            val = card[idx]
            is_free = val == "FREE"
            if bw_mode:
                bg = "#111" if is_free else ("white" if (r+c)%2==0 else "#f0f0f0")
                txt_color = "white" if is_free else "#111"
                border = "3px solid #111"
            else:
                bg = "linear-gradient(135deg,#ffd6e7,#ffecb3)" if is_free \
                     else CELL_PALETTE[idx % len(CELL_PALETTE)]
                txt_color = "#c0392b" if is_free else "white"
                border = "3px solid rgba(255,255,255,0.6)"
            display_val = "★ FREE ★" if is_free else val
            row_html += (
                f'<td style="width:{cell_size}px;height:{cell_size}px;background:{bg};'
                f'border-radius:12px;border:{border};text-align:center;'
                f'vertical-align:middle;font-size:{font_size}rem;font-weight:900;'
                f'color:{txt_color};padding:4px;word-break:break-word;'
                f'font-family:Fredoka One,Nunito,sans-serif;">{display_val}</td>'
            )
        row_html += "</tr>"
        rows_html += row_html

    card_bg = "#222" if bw_mode else "white"
    title_color = "white" if bw_mode else "#5c35d9"
    return f"""
    <div class="bingo-card" style="background:{card_bg};">
        <div class="bingo-card-title" style="color:{title_color};">
            🎱 BINGO &mdash; Card #{card_num}
        </div>
        <table style="border-collapse:separate;border-spacing:5px;margin:auto;">
            {rows_html}
        </table>
    </div>"""


# ══════════════════════════════════════════════════════════════════════════════
#  PDF GENERATION (reportlab.platypus — 2 cards per A4 page)
# ══════════════════════════════════════════════════════════════════════════════

def generate_pdf(cards, grid_size, bw_mode):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate, Table, TableStyle,
            Paragraph, Spacer, KeepTogether
        )
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER

        buf = io.BytesIO()
        PAGE_W, PAGE_H = A4
        MARGIN = 12 * mm

        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=MARGIN, rightMargin=MARGIN,
            topMargin=MARGIN, bottomMargin=MARGIN,
        )

        usable_w = PAGE_W - 2 * MARGIN
        col_w    = usable_w / grid_size
        half_h   = (PAGE_H - 2 * MARGIN - 20 * mm) / 2
        row_h    = min((half_h - 14 * mm) / grid_size, col_w * 0.88)

        title_color = colors.HexColor("#111111" if bw_mode else "#5c35d9")
        title_style = ParagraphStyle(
            "CardTitle", fontName="Helvetica-Bold", fontSize=16,
            textColor=title_color, alignment=TA_CENTER,
            spaceAfter=3*mm, spaceBefore=2*mm,
        )
        cut_style = ParagraphStyle(
            "CutLine", fontName="Helvetica", fontSize=7,
            textColor=colors.HexColor("#aaaaaa"), alignment=TA_CENTER,
            spaceAfter=5*mm, spaceBefore=5*mm,
        )

        PDF_COLORS = [
            "#FF6B6B","#FF9F43","#FFEAA7","#A8E6CF","#81ECEC",
            "#74B9FF","#A29BFE","#FD79A8","#FDCB6E","#55EFC4",
            "#E17055","#0984E3","#6C5CE7","#00CEC9","#E84393",
        ]

        def make_card_table(card):
            data, ts_cmds = [], [
                ("ALIGN",          (0,0), (-1,-1), "CENTER"),
                ("VALIGN",         (0,0), (-1,-1), "MIDDLE"),
                ("LEFTPADDING",    (0,0), (-1,-1), 3),
                ("RIGHTPADDING",   (0,0), (-1,-1), 3),
                ("TOPPADDING",     (0,0), (-1,-1), 3),
                ("BOTTOMPADDING",  (0,0), (-1,-1), 3),
            ]
            for r in range(grid_size):
                row = []
                for c in range(grid_size):
                    idx     = r * grid_size + c
                    val     = card[idx]
                    is_free = val == "FREE"
                    if bw_mode:
                        txt_c = colors.white if is_free else colors.black
                        bg    = colors.HexColor("#111111") if is_free \
                                else (colors.white if (r+c)%2==0 else colors.HexColor("#e0e0e0"))
                    else:
                        txt_c = colors.HexColor("#c0392b") if is_free else colors.white
                        bg    = colors.HexColor("#ffeaa7") if is_free \
                                else colors.HexColor(PDF_COLORS[idx % len(PDF_COLORS)])

                    cell_fs = max(7, 14 - grid_size)
                    p_style = ParagraphStyle(
                        f"cs{idx}", fontName="Helvetica-Bold", fontSize=cell_fs,
                        textColor=txt_c, alignment=TA_CENTER, leading=cell_fs+4,
                    )
                    row.append(Paragraph(val, p_style))
                    ts_cmds.append(("BACKGROUND", (c,r), (c,r), bg))
                data.append(row)

            grid_color = colors.black if bw_mode else colors.white
            ts_cmds.append(("GRID", (0,0), (-1,-1), 1.5, grid_color))
            t = Table(data, colWidths=[col_w]*grid_size, rowHeights=[row_h]*grid_size)
            t.setStyle(TableStyle(ts_cmds))
            return t

        story = []
        cut_text = ("  ✂  - - - - - - - - - - - - - - - - - - - - - "
                    "cut here"
                    " - - - - - - - - - - - - - - - - - - - - - ✂  ")

        for i, card in enumerate(cards):
            story.append(KeepTogether([
                Paragraph(f"✦  BINGO  —  Card #{i+1}  ✦", title_style),
                make_card_table(card),
            ]))
            is_last         = (i == len(cards) - 1)
            is_first_of_pair = (i % 2 == 0)
            if not is_last and is_first_of_pair:
                story.append(Paragraph(cut_text, cut_style))
            elif not is_last:
                story.append(Spacer(1, 4*mm))

        doc.build(story)
        buf.seek(0)
        return buf.getvalue(), None

    except ImportError as exc:
        return None, f"reportlab not installed: {exc}"
    except Exception as exc:
        return None, str(exc)


# ══════════════════════════════════════════════════════════════════════════════
#  PRINTABLE HTML FALLBACK
# ══════════════════════════════════════════════════════════════════════════════

def generate_html(cards, grid_size, bw_mode):
    cards_html = ""
    for i, card in enumerate(cards):
        cell_size = max(55, min(95, 420 // grid_size))
        font_size = max(11, min(22, cell_size // 4))
        rows = ""
        for r in range(grid_size):
            rows += "<tr>"
            for c in range(grid_size):
                idx     = r * grid_size + c
                val     = card[idx]
                is_free = val == "FREE"
                if bw_mode:
                    bg  = "#111" if is_free else ("white" if (r+c)%2==0 else "#e8e8e8")
                    col = "white" if is_free else "#111"
                    bdr = "2px solid #111"
                else:
                    bg  = "linear-gradient(135deg,#ffd6e7,#ffecb3)" if is_free \
                          else CELL_PALETTE[idx % len(CELL_PALETTE)]
                    col = "#c0392b" if is_free else "white"
                    bdr = "2px solid rgba(255,255,255,0.5)"
                rows += (
                    f'<td style="width:{cell_size}px;height:{cell_size}px;background:{bg};'
                    f'border-radius:12px;border:{bdr};text-align:center;vertical-align:middle;'
                    f'font-size:{font_size}px;font-weight:900;color:{col};'
                    f'word-break:break-word;font-family:Fredoka One,Arial,sans-serif;">'
                    f'{val}</td>'
                )
            rows += "</tr>"
        page_break = '<div style="page-break-before:always;"></div>' \
                     if i > 0 and i % 2 == 0 else ""
        cut = (
            '<div style="text-align:center;color:#aaa;font-size:11px;margin:10px 0;">'
            '&#9986; &mdash; &mdash; &mdash; cut here &mdash; &mdash; &mdash; &#9986;</div>'
        ) if i % 2 == 0 and i < len(cards) - 1 else ""
        title_color = "white" if bw_mode else "#5c35d9"
        cards_html += f"""
        {page_break}
        <div style="text-align:center;font-family:'Fredoka One',Arial,sans-serif;
                    font-size:22px;color:{title_color};margin:14px 0 8px;">
            ✦ BINGO &mdash; Card #{i+1} ✦
        </div>
        <div style="text-align:center;">
            <table style="border-collapse:separate;border-spacing:5px;display:inline-table;">
                {rows}
            </table>
        </div>
        {cut}"""

    bg_body = "#222" if bw_mode else "#f0f4ff"
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Bingo Cards</title>
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap" rel="stylesheet">
<style>
  body {{ background:{bg_body}; font-family:'Fredoka One',Arial,sans-serif; margin:20px; }}
  @media print {{ .no-print {{ display:none; }} body {{ margin:10mm; background:white; }} }}
</style></head><body>
<div class="no-print" style="text-align:center;margin-bottom:20px;">
  <button onclick="window.print()"
    style="background:#5c35d9;color:white;border:none;border-radius:14px;
           padding:12px 28px;font-size:17px;font-weight:700;cursor:pointer;">
    Print Cards
  </button>
</div>
{cards_html}
</body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
#  APP HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<h1 class="app-title">🎉 Bingo Builder for Kids 🎱</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-sub">✨ Create magical bingo cards for your classroom in seconds! ✨</p>',
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_create, tab_caller = st.tabs(["🃏  Create Bingo Sheets", "🎡  Play Caller"])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — CREATE BINGO SHEETS
# ══════════════════════════════════════════════════════════════════════════════
with tab_create:

    inp_words, inp_numbers = st.tabs(["🔤 Words Mode", "🔢 Numbers Mode"])

    with inp_words:
        st.markdown("#### 📋 Quick Templates")
        t_cols = st.columns(4)
        for idx, (label, vals) in enumerate(TEMPLATES.items()):
            with t_cols[idx]:
                if st.button(f"📋 {label}", key=f"tpl_{idx}", use_container_width=True):
                    st.session_state.words_input = ", ".join(vals)
                    st.session_state.error_msg   = None

        words_raw = st.text_area(
            "Enter your words (comma or newline separated):",
            value=st.session_state.words_input,
            height=140,
            placeholder="apple, banana, cat, dog…\nor one per line",
            key="words_textarea",
        )
        st.session_state.words_input = words_raw
        raw_parts   = [w.strip() for part in words_raw.replace("\n",",").split(",") for w in [part.strip()] if w]
        words_items = list(dict.fromkeys(filter(None, raw_parts)))
        st.caption(f"✅ {len(words_items)} unique words detected")

    with inp_numbers:
        nc1, nc2 = st.columns(2)
        with nc1:
            num_start = st.number_input("Start number:", value=1,  min_value=0,    max_value=9999, key="num_start")
        with nc2:
            num_end   = st.number_input("End number:",   value=50, min_value=1,    max_value=9999, key="num_end")
        if int(num_end) > int(num_start):
            num_items = [str(i) for i in range(int(num_start), int(num_end)+1)]
            st.caption(f"✅ {len(num_items)} numbers ({int(num_start)}–{int(num_end)})")
        else:
            num_items = []
            st.warning("End must be greater than Start.")

    mode_sel     = st.radio("Active input mode:", ["🔤 Words Mode", "🔢 Numbers Mode"],
                             horizontal=True, label_visibility="collapsed")
    active_items = words_items if "Words" in mode_sel else num_items

    st.markdown("---")
    st.markdown("### ⚙️ Bingo Settings")

    sc1, sc2, sc3, sc4 = st.columns([2, 2, 2, 2])
    with sc1:
        grid_size = st.selectbox("Grid Size", [3,4,5,6,7,8], index=2,
                                  format_func=lambda x: f"{x}×{x}", key="grid_sel")
    with sc2:
        num_cards = st.slider("Number of Cards", 10, 15, 10)
    with sc3:
        if grid_size >= 5:
            free_space = st.toggle("⭐ FREE SPACE (center)", value=True)
        else:
            free_space = False
            st.info("FREE SPACE: 5×5+ only")
    with sc4:
        bw_mode = st.toggle("⬛ Black & White Mode", value=False)

    g_col, _ = st.columns([2, 5])
    with g_col:
        if st.button("🎲 Generate Bingo Cards!", type="primary", use_container_width=True):
            st.session_state.error_msg = None
            cards, err = generate_cards(active_items, grid_size, num_cards, free_space)
            if err:
                st.session_state.error_msg = err
                st.session_state.cards     = None
            else:
                st.session_state.cards           = cards
                st.session_state.grid_size        = grid_size
                st.session_state.items            = list(active_items)
                st.session_state.caller_pool      = fisher_yates_shuffle(active_items)
                st.session_state.caller_history   = []
                st.session_state.caller_current   = None
                st.session_state.caller_call_count = 0
                st.session_state.auto_running     = False
                st.session_state.show_win         = False

    if st.session_state.error_msg:
        st.markdown(f'<div class="error-box">❌ {st.session_state.error_msg}</div>',
                    unsafe_allow_html=True)

    if st.session_state.cards:
        cards = st.session_state.cards
        gs    = st.session_state.grid_size
        st.markdown(f"### 🃏 Your {len(cards)} Bingo Cards")

        cols_per_row = 2 if gs <= 5 else 1
        for row_start in range(0, len(cards), cols_per_row):
            cols = st.columns(cols_per_row)
            for ci, card_idx in enumerate(range(row_start, min(row_start+cols_per_row, len(cards)))):
                with cols[ci]:
                    st.markdown(render_card_html(cards[card_idx], gs, card_idx+1, bw_mode),
                                unsafe_allow_html=True)

        st.markdown("---\n### 💾 Download")
        dl1, dl2 = st.columns(2)
        with dl1:
            pdf_bytes, pdf_err = generate_pdf(cards, gs, bw_mode)
            if pdf_bytes:
                st.download_button("📥 Download PDF (2 cards per page)",
                                   data=pdf_bytes, file_name="bingo_cards.pdf",
                                   mime="application/pdf", use_container_width=True)
            else:
                st.caption(f"⚠️ PDF unavailable ({pdf_err}). Use HTML below.")
        with dl2:
            st.download_button("🖨️ Download Printable HTML",
                               data=generate_html(cards, gs, bw_mode).encode("utf-8"),
                               file_name="bingo_cards.html", mime="text/html",
                               use_container_width=True)
        if bw_mode:
            st.info("⬛ Black & White mode active — PDF and HTML print in high-contrast B&W.")


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — PLAY CALLER  (Disney Magic Stage)
# ══════════════════════════════════════════════════════════════════════════════
with tab_caller:

    # ── Guard: need cards first ──────────────────────────────────────────────
    if not st.session_state.items:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;">
            <div style="font-size:5rem;">🎱</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#5c35d9;margin:12px 0;">
                No items yet!
            </div>
            <div style="color:#888;font-size:1.1rem;">
                Go to <strong>Create Bingo Sheets</strong>, generate your cards,
                then come back to play!
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ── Derived state ────────────────────────────────────────────────────────
    pool      = st.session_state.caller_pool
    history   = st.session_state.caller_history
    history_set = set(history)
    current   = st.session_state.caller_current
    remaining = [x for x in pool if x not in history_set]
    total     = len(pool)
    called    = len(history)
    pct       = int(called / total * 100) if total else 0
    all_done  = len(remaining) == 0 and called > 0

    # Auto-stop on completion
    if all_done:
        st.session_state.auto_running = False
        st.session_state.show_win     = True

    # ── WIN SCREEN (rendered before controls) ────────────────────────────────
    if st.session_state.show_win:
        st.markdown(win_screen_html(), unsafe_allow_html=True)

        # "Play Again" is handled via a Streamlit button below the overlay
        pa_col, _ = st.columns([2, 5])
        with pa_col:
            if st.button("🎮 Play Again", type="primary", use_container_width=True):
                st.session_state.caller_pool       = fisher_yates_shuffle(st.session_state.items)
                st.session_state.caller_history    = []
                st.session_state.caller_current    = None
                st.session_state.caller_call_count = 0
                st.session_state.auto_running      = False
                st.session_state.show_win          = False
                st.rerun()
        st.stop()

    # ── Controls row ─────────────────────────────────────────────────────────
    st.markdown("#### 🎮 Caller Mode")
    mode_col, speed_col, reset_col = st.columns([3, 3, 2])

    with mode_col:
        caller_mode = st.radio(
            "Mode", ["Manual", "Auto"], horizontal=True,
            index=0 if st.session_state.caller_mode == "manual" else 1,
            label_visibility="collapsed",
        )
        st.session_state.caller_mode = caller_mode.lower()

    auto_interval = st.session_state.auto_interval
    if st.session_state.caller_mode == "auto":
        with speed_col:
            auto_interval = st.slider("⏱ Call every (seconds)", 1, 10, auto_interval)
            st.session_state.auto_interval = auto_interval

    with reset_col:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.caller_pool       = fisher_yates_shuffle(st.session_state.items)
            st.session_state.caller_history    = []
            st.session_state.caller_current    = None
            st.session_state.caller_call_count = 0
            st.session_state.auto_running      = False
            st.session_state.show_win          = False
            st.rerun()

    st.markdown("---")

    # ── Magic stage display — uses st.empty() for targeted updates ───────────
    stage_slot = st.empty()
    stage_slot.markdown(
        caller_display_html(current, pct, called, total,
                            st.session_state.caller_call_count),
        unsafe_allow_html=True,
    )

    # ── Action buttons ───────────────────────────────────────────────────────
    if st.session_state.caller_mode == "manual":
        btn_col, _ = st.columns([2, 5])
        with btn_col:
            if st.button("▶ Next Item", type="primary", use_container_width=True,
                         disabled=(len(remaining) == 0)):
                pick = remaining[random.randint(0, len(remaining)-1)]
                st.session_state.caller_current    = pick
                st.session_state.caller_call_count += 1
                st.session_state.caller_history.append(pick)
                st.rerun()
    else:
        ac1, ac2, _ = st.columns([2, 2, 4])
        with ac1:
            if not st.session_state.auto_running:
                if st.button("▶ Start Auto", type="primary", use_container_width=True,
                             disabled=(len(remaining) == 0)):
                    st.session_state.auto_running   = True
                    st.session_state.auto_last_tick = time.time()
                    st.rerun()
            else:
                if st.button("⏸ Pause", use_container_width=True):
                    st.session_state.auto_running = False
                    st.rerun()
        with ac2:
            if st.session_state.auto_running:
                st.markdown(
                    '<div class="live-badge">'
                    '<div class="live-dot"></div>LIVE'
                    '</div>',
                    unsafe_allow_html=True,
                )

    # ── Auto-advance logic (optimised: single sleep, targeted rerun) ─────────
    # Strategy: sleep the REMAINING time until next tick (capped at 0.8 s so
    # Pause stays responsive), then rerun ONLY the caller section via st.rerun().
    # This avoids the old double-sleep pattern and keeps the UI snappy.
    if st.session_state.auto_running and remaining:
        elapsed = time.time() - st.session_state.auto_last_tick

        if elapsed >= auto_interval:
            # ── Time to call the next item ──
            # Add slight random variance (±15%) for a more natural feel
            variance    = auto_interval * 0.15
            next_gap    = auto_interval + random.uniform(-variance, variance)
            pick        = remaining[random.randint(0, len(remaining)-1)]
            st.session_state.caller_current     = pick
            st.session_state.caller_call_count += 1
            st.session_state.caller_history.append(pick)
            st.session_state.auto_last_tick     = time.time()
            # Update the stage slot immediately (no full rerun needed for display)
            new_remaining = [x for x in pool if x not in set(st.session_state.caller_history)]
            new_pct  = int(len(st.session_state.caller_history) / total * 100)
            stage_slot.markdown(
                caller_display_html(pick, new_pct,
                                    len(st.session_state.caller_history), total,
                                    st.session_state.caller_call_count),
                unsafe_allow_html=True,
            )
            # Short pause so animation plays, then lightweight rerun
            time.sleep(0.12)
            st.rerun()
        else:
            # Not time yet — sleep just long enough then rerun to re-check
            wait = min(auto_interval - elapsed, 0.8)
            time.sleep(wait)
            st.rerun()

    # ── Call history ─────────────────────────────────────────────────────────
    if history:
        st.markdown("---")
        st.markdown("**📜 Call History** (most recent first):")
        chips = " ".join(
            f'<span class="history-chip">{item}</span>'
            for item in reversed(history)
        )
        st.markdown(chips, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#bbb;font-size:0.82rem;'>"
    "🎉 Bingo Builder for Kids &mdash; Made with ❤️ using Streamlit &amp; reportlab"
    "</p>",
    unsafe_allow_html=True,
)
