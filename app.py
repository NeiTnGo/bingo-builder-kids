import streamlit as st
import random
import io
import time

# ─── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="🎉 Bingo Builder for Kids",
    page_icon="🎱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Fredoka+One&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
.main { background: linear-gradient(135deg, #f0f4ff 0%, #fdf0ff 100%); }

/* ── App title ── */
.app-title {
    text-align: center;
    font-family: 'Fredoka One', cursive;
    font-size: 3rem;
    background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff, #c77dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
}
.app-sub { text-align:center; color:#888; font-size:1.05rem; margin-top:0; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px; background: #e8e0ff; border-radius: 18px; padding: 6px;
}
.stTabs [data-baseweb="tab"] {
    background: white; border-radius: 14px; font-weight: 700;
    font-size: 1.05rem; color: #5c35d9; padding: 10px 28px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#5c35d9,#9b59b6) !important;
    color: white !important;
}

/* ── Settings panel ── */
.settings-box {
    background: white; border-radius: 22px; padding: 22px; margin-bottom: 18px;
    box-shadow: 0 4px 20px rgba(92,53,217,0.12); border: 2px solid #e8e0ff;
}

/* ── Bingo card preview ── */
.bingo-card {
    background: white; border-radius: 22px; padding: 14px; margin: 8px;
    box-shadow: 0 6px 20px rgba(92,53,217,0.13); border: 3px solid #c9b8ff;
}
.bingo-card-title {
    text-align: center; font-family: 'Fredoka One', cursive;
    font-size: 1.2rem; color: #5c35d9; margin-bottom: 10px; letter-spacing:1px;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 16px; font-weight: 700; font-size: 1rem;
    padding: 9px 22px; border: none; transition: all 0.2s;
}
.stButton > button:hover { transform: scale(1.05); box-shadow: 0 4px 14px rgba(0,0,0,0.15); }

/* ── Error box ── */
.error-box {
    background: #ffe0e0; border: 2px solid #ffb3b3; border-radius: 14px;
    padding: 14px 20px; color: #c0392b; font-weight: 700; margin: 10px 0;
}

/* ── History chips ── */
.history-chip {
    display: inline-block; background: #e8e0ff; color: #5c35d9;
    border-radius: 22px; padding: 5px 14px; margin: 3px;
    font-weight: 700; font-size: 0.88rem;
}

/* ══════════════════════════════════════════════════════════════════════════
   PLAY CALLER ANIMATIONS
   ══════════════════════════════════════════════════════════════════════════ */
@keyframes bgShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes popIn {
    0%   { transform: scale(0.4) rotate(-8deg); opacity: 0; }
    60%  { transform: scale(1.15) rotate(3deg); opacity: 1; }
    80%  { transform: scale(0.95) rotate(-1deg); }
    100% { transform: scale(1) rotate(0deg); opacity: 1; }
}
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    30%       { transform: translateY(-12px); }
    60%       { transform: translateY(-5px); }
}

.caller-wrapper {
    background: linear-gradient(270deg, #ff6b6b, #ffd93d, #6bcb77, #4d96ff, #c77dff, #ff6b6b);
    background-size: 400% 400%;
    animation: bgShift 6s ease infinite;
    border-radius: 28px;
    padding: 14px;
    margin: 16px 0;
    box-shadow: 0 10px 40px rgba(0,0,0,0.18);
}
.caller-inner {
    background: rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 30px 20px;
    text-align: center;
}
.caller-number {
    font-family: 'Fredoka One', cursive;
    font-size: 7rem;
    color: white;
    text-shadow: 3px 4px 0 rgba(0,0,0,0.18);
    line-height: 1;
    animation: popIn 0.55s cubic-bezier(.36,.07,.19,.97) both;
    display: block;
}
.caller-label {
    font-size: 1.2rem; color: rgba(255,255,255,0.9); font-weight: 700;
    margin-top: 8px; letter-spacing:1px;
    animation: bounce 1.2s ease 0.6s 2;
    display: inline-block;
}
.caller-idle {
    font-family: 'Fredoka One', cursive;
    font-size: 2.5rem; color: rgba(255,255,255,0.6);
    text-align: center; padding: 40px 0;
}
.progress-bar-outer {
    background: rgba(255,255,255,0.3); border-radius: 20px;
    height: 14px; margin: 14px 0 4px;
    overflow: hidden;
}
.progress-bar-inner {
    height: 14px; border-radius: 20px;
    background: white;
    transition: width 0.5s ease;
}
.auto-indicator {
    display: inline-block; background: #ff6b6b; color: white;
    border-radius: 20px; padding: 4px 14px; font-weight: 700;
    font-size: 0.85rem; margin-left: 8px; animation: bounce 1s ease infinite;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS & TEMPLATES
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

# Bright kid-friendly cell colors (color mode)
CELL_PALETTE = [
    "#FF6B6B","#FF9F43","#FFEAA7","#A8E6CF","#81ECEC",
    "#74B9FF","#A29BFE","#FD79A8","#FDCB6E","#55EFC4",
    "#E17055","#0984E3","#6C5CE7","#00CEC9","#E84393",
]

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE INIT
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
    "caller_mode": "manual",
    "auto_running": False,
    "auto_last_tick": 0.0,
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
            f"for a {grid_size}x{grid_size} grid (you have {len(items)})."
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


# ══════════════════════════════════════════════════════════════════════════════
#  HTML CARD PREVIEW (in-app)
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
                bg = "#111" if is_free else ("white" if (r + c) % 2 == 0 else "#f0f0f0")
                txt_color = "white" if is_free else "#111"
                border = "3px solid #111"
            else:
                bg = "linear-gradient(135deg,#ffd6e7,#ffecb3)" if is_free \
                     else CELL_PALETTE[idx % len(CELL_PALETTE)]
                txt_color = "#c0392b" if is_free else "white"
                border = "3px solid rgba(255,255,255,0.6)"

            display_val = ("★ FREE ★" if is_free else val)
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
#  PDF GENERATION  (reportlab.platypus – 2 cards per A4 page)
# ══════════════════════════════════════════════════════════════════════════════

def generate_pdf(cards, grid_size, bw_mode):
    """Returns (pdf_bytes, error_string). error_string is None on success."""
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

        # ── Computed dimensions ──────────────────────────────────────────────
        usable_w = PAGE_W - 2 * MARGIN
        col_w    = usable_w / grid_size
        # Each half-page minus title + cut-line space
        half_h   = (PAGE_H - 2 * MARGIN - 20 * mm) / 2
        row_h    = min((half_h - 14 * mm) / grid_size, col_w * 0.88)

        # ── Styles ───────────────────────────────────────────────────────────
        title_color = colors.HexColor("#111111" if bw_mode else "#5c35d9")
        title_style = ParagraphStyle(
            "CardTitle",
            fontName="Helvetica-Bold", fontSize=16,
            textColor=title_color, alignment=TA_CENTER,
            spaceAfter=3 * mm, spaceBefore=2 * mm,
        )
        cut_style = ParagraphStyle(
            "CutLine",
            fontName="Helvetica", fontSize=7,
            textColor=colors.HexColor("#aaaaaa"),
            alignment=TA_CENTER,
            spaceAfter=5 * mm, spaceBefore=5 * mm,
        )

        PDF_COLORS = [
            "#FF6B6B","#FF9F43","#FFEAA7","#A8E6CF","#81ECEC",
            "#74B9FF","#A29BFE","#FD79A8","#FDCB6E","#55EFC4",
            "#E17055","#0984E3","#6C5CE7","#00CEC9","#E84393",
        ]

        # ── Card table builder ───────────────────────────────────────────────
        def make_card_table(card):
            data = []
            ts_cmds = [
                ("ALIGN",    (0,0), (-1,-1), "CENTER"),
                ("VALIGN",   (0,0), (-1,-1), "MIDDLE"),
                ("LEFTPADDING",   (0,0), (-1,-1), 3),
                ("RIGHTPADDING",  (0,0), (-1,-1), 3),
                ("TOPPADDING",    (0,0), (-1,-1), 3),
                ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ]
            for r in range(grid_size):
                row = []
                for c in range(grid_size):
                    idx  = r * grid_size + c
                    val  = card[idx]
                    is_free = val == "FREE"
                    display_val = "FREE" if is_free else val

                    # Choose text color
                    if bw_mode:
                        if is_free:
                            txt_c = colors.white
                        elif (r + c) % 2 == 0:
                            txt_c = colors.black
                        else:
                            txt_c = colors.black
                    else:
                        txt_c = colors.HexColor("#c0392b") if is_free else colors.white

                    cell_fs = max(7, 14 - grid_size)
                    p_style = ParagraphStyle(
                        f"cs{idx}",
                        fontName="Helvetica-Bold",
                        fontSize=cell_fs,
                        textColor=txt_c,
                        alignment=TA_CENTER,
                        leading=cell_fs + 4,
                    )
                    row.append(Paragraph(display_val, p_style))

                    # Cell background
                    if bw_mode:
                        bg = colors.HexColor("#111111") if is_free \
                             else (colors.white if (r+c) % 2 == 0 else colors.HexColor("#e0e0e0"))
                    else:
                        bg = colors.HexColor("#ffeaa7") if is_free \
                             else colors.HexColor(PDF_COLORS[idx % len(PDF_COLORS)])

                    ts_cmds.append(("BACKGROUND", (c,r), (c,r), bg))

                data.append(row)

            grid_color = colors.black if bw_mode else colors.white
            ts_cmds.append(("GRID", (0,0), (-1,-1), 1.5, grid_color))

            t = Table(
                data,
                colWidths=[col_w] * grid_size,
                rowHeights=[row_h] * grid_size,
            )
            t.setStyle(TableStyle(ts_cmds))
            return t

        # ── Build story ──────────────────────────────────────────────────────
        story = []
        cut_text = (
            "  ✂  - - - - - - - - - - - - - - - - - - - - - "
            "cut here"
            " - - - - - - - - - - - - - - - - - - - - - ✂  "
        )

        for i, card in enumerate(cards):
            title = Paragraph(f"✦  BINGO  —  Card #{i + 1}  ✦", title_style)
            tbl   = make_card_table(card)
            block = KeepTogether([title, tbl])
            story.append(block)

            is_last = (i == len(cards) - 1)
            is_first_of_pair = (i % 2 == 0)

            if not is_last and is_first_of_pair:
                # Dashed cut line between the two cards on the same page
                story.append(Paragraph(cut_text, cut_style))
            elif not is_last and not is_first_of_pair:
                # After second card → small spacer (page break is handled by platypus)
                story.append(Spacer(1, 4 * mm))

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
                idx = r * grid_size + c
                val = card[idx]
                is_free = val == "FREE"
                display_val = "FREE" if is_free else val
                if bw_mode:
                    bg = "#111" if is_free else ("white" if (r+c)%2==0 else "#e8e8e8")
                    col = "white" if is_free else "#111"
                    bdr = "2px solid #111"
                else:
                    bg = "linear-gradient(135deg,#ffd6e7,#ffecb3)" if is_free \
                         else CELL_PALETTE[idx % len(CELL_PALETTE)]
                    col = "#c0392b" if is_free else "white"
                    bdr = "2px solid rgba(255,255,255,0.5)"
                rows += (
                    f'<td style="width:{cell_size}px;height:{cell_size}px;background:{bg};'
                    f'border-radius:12px;border:{bdr};text-align:center;vertical-align:middle;'
                    f'font-size:{font_size}px;font-weight:900;color:{col};'
                    f'word-break:break-word;font-family:Fredoka One,Arial,sans-serif;">'
                    f'{display_val}</td>'
                )
            rows += "</tr>"

        page_break = '<div style="page-break-before:always;"></div>' \
                     if i > 0 and i % 2 == 0 else ""
        cut = (
            '<div style="text-align:center;color:#aaa;font-size:11px;'
            'margin:10px 0;letter-spacing:2px;">'
            '&#9986; &mdash; &mdash; &mdash; &mdash; &mdash; &mdash; '
            '&mdash; &mdash; cut here &mdash; &mdash; &mdash; &mdash; '
            '&mdash; &mdash; &mdash; &mdash; &#9986;</div>'
        ) if i % 2 == 0 and i < len(cards) - 1 else ""

        title_color = "white" if bw_mode else "#5c35d9"
        cards_html += f"""
        {page_break}
        <div style="text-align:center;font-family:'Fredoka One',Arial,sans-serif;
                    font-size:22px;color:{title_color};margin:14px 0 8px;">
            ✦ BINGO &mdash; Card #{i + 1} ✦
        </div>
        <div style="text-align:center;">
            <table style="border-collapse:separate;border-spacing:5px;display:inline-table;">
                {rows}
            </table>
        </div>
        {cut}"""

    bg_body = "#222" if bw_mode else "#f0f4ff"
    return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>Bingo Cards</title>
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap" rel="stylesheet">
<style>
  body {{ background:{bg_body}; font-family:'Fredoka One',Arial,sans-serif; margin:20px; }}
  @media print {{ .no-print {{ display:none; }} body {{ margin:10mm; background:white; }} }}
</style>
</head><body>
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
    '<p class="app-sub">Create magical bingo cards for your classroom in seconds!</p>',
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_create, tab_caller = st.tabs(["🃏  Create Bingo Sheets", "🎡  Play Caller"])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1: CREATE BINGO SHEETS
# ══════════════════════════════════════════════════════════════════════════════
with tab_create:

    # ── Input mode sub-tabs ──────────────────────────────────────────────────
    inp_words, inp_numbers = st.tabs(["🔤 Words Mode", "🔢 Numbers Mode"])

    with inp_words:
        st.markdown("#### Quick Templates")
        t_cols = st.columns(4)
        for idx, (label, vals) in enumerate(TEMPLATES.items()):
            with t_cols[idx]:
                if st.button(f"📋 {label}", key=f"tpl_{idx}", use_container_width=True):
                    st.session_state.words_input = ", ".join(vals)
                    st.session_state.error_msg = None

        words_raw = st.text_area(
            "Enter your words (comma or newline separated):",
            value=st.session_state.words_input,
            height=140,
            placeholder="apple, banana, cat, dog…\nor one per line",
            key="words_textarea",
        )
        st.session_state.words_input = words_raw
        raw_parts = [
            w.strip()
            for part in words_raw.replace("\n", ",").split(",")
            for w in [part.strip()] if w
        ]
        words_items = list(dict.fromkeys(filter(None, raw_parts)))
        st.caption(f"✅ {len(words_items)} unique words detected")

    with inp_numbers:
        nc1, nc2 = st.columns(2)
        with nc1:
            num_start = st.number_input("Start number:", value=1, min_value=0,
                                         max_value=9999, key="num_start")
        with nc2:
            num_end = st.number_input("End number:", value=50, min_value=1,
                                       max_value=9999, key="num_end")
        if int(num_end) > int(num_start):
            num_items = [str(i) for i in range(int(num_start), int(num_end) + 1)]
            st.caption(f"✅ {len(num_items)} numbers ({int(num_start)}–{int(num_end)})")
        else:
            num_items = []
            st.warning("End must be greater than Start.")

    # ── Active mode selector ─────────────────────────────────────────────────
    mode_sel = st.radio(
        "Active input mode:",
        ["🔤 Words Mode", "🔢 Numbers Mode"],
        horizontal=True,
        label_visibility="collapsed",
    )
    active_items = words_items if "Words" in mode_sel else num_items

    st.markdown("---")

    # ── Bingo Settings ───────────────────────────────────────────────────────
    st.markdown("### ⚙️ Bingo Settings")
    sc1, sc2, sc3, sc4 = st.columns([2, 2, 2, 2])
    with sc1:
        grid_size = st.selectbox(
            "Grid Size", [3, 4, 5, 6, 7, 8],
            index=2, format_func=lambda x: f"{x}x{x}", key="grid_sel",
        )
    with sc2:
        num_cards = st.slider("Number of Cards", 10, 15, 10)
    with sc3:
        if grid_size >= 5:
            free_space = st.toggle("FREE SPACE (center)", value=True)
        else:
            free_space = False
            st.info("FREE SPACE: 5x5+ only")
    with sc4:
        bw_mode = st.toggle("Black & White Mode", value=False)

    # ── Generate ─────────────────────────────────────────────────────────────
    g_col, _ = st.columns([2, 5])
    with g_col:
        if st.button("🎲 Generate Bingo Cards!", type="primary", use_container_width=True):
            st.session_state.error_msg = None
            cards, err = generate_cards(active_items, grid_size, num_cards, free_space)
            if err:
                st.session_state.error_msg = err
                st.session_state.cards = None
            else:
                st.session_state.cards       = cards
                st.session_state.grid_size   = grid_size
                st.session_state.items       = list(active_items)
                st.session_state.caller_pool = fisher_yates_shuffle(active_items)
                st.session_state.caller_history = []
                st.session_state.caller_current = None
                st.session_state.auto_running   = False

    if st.session_state.error_msg:
        st.markdown(
            f'<div class="error-box">❌ {st.session_state.error_msg}</div>',
            unsafe_allow_html=True,
        )

    # ── Display Cards ────────────────────────────────────────────────────────
    if st.session_state.cards:
        cards = st.session_state.cards
        gs    = st.session_state.grid_size
        st.markdown(f"### 🃏 Your {len(cards)} Bingo Cards")

        cols_per_row = 2 if gs <= 5 else 1
        for row_start in range(0, len(cards), cols_per_row):
            cols = st.columns(cols_per_row)
            for ci, card_idx in enumerate(
                range(row_start, min(row_start + cols_per_row, len(cards)))
            ):
                with cols[ci]:
                    st.markdown(
                        render_card_html(cards[card_idx], gs, card_idx + 1, bw_mode),
                        unsafe_allow_html=True,
                    )

        # ── Downloads ────────────────────────────────────────────────────────
        st.markdown("---\n### 💾 Download")
        dl1, dl2 = st.columns(2)

        with dl1:
            pdf_bytes, pdf_err = generate_pdf(cards, gs, bw_mode)
            if pdf_bytes:
                st.download_button(
                    label="📥 Download PDF (2 cards per page)",
                    data=pdf_bytes,
                    file_name="bingo_cards.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                st.caption(f"⚠️ PDF unavailable ({pdf_err}). Use HTML below.")

        with dl2:
            html_bytes = generate_html(cards, gs, bw_mode).encode("utf-8")
            st.download_button(
                label="🖨️ Download Printable HTML",
                data=html_bytes,
                file_name="bingo_cards.html",
                mime="text/html",
                use_container_width=True,
            )

        if bw_mode:
            st.info("⬛ Black & White mode is active — PDF and HTML will print in high-contrast B&W.")


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2: PLAY CALLER
# ══════════════════════════════════════════════════════════════════════════════
with tab_caller:

    if not st.session_state.items:
        st.info(
            "👆 Go to **Create Bingo Sheets**, generate your cards first, "
            "then come back here to play!"
        )
        st.stop()

    pool      = st.session_state.caller_pool
    history   = st.session_state.caller_history
    current   = st.session_state.caller_current
    remaining = [x for x in pool if x not in set(history)]
    total     = len(pool)
    called    = len(history)
    pct       = int(called / total * 100) if total else 0

    # ── Mode selector + controls row ─────────────────────────────────────────
    st.markdown("#### 🎮 Caller Mode")
    mode_col, speed_col, reset_col = st.columns([3, 3, 2])

    with mode_col:
        caller_mode = st.radio(
            "Mode", ["Manual", "Auto"],
            horizontal=True,
            index=0 if st.session_state.caller_mode == "manual" else 1,
            label_visibility="collapsed",
        )
        st.session_state.caller_mode = caller_mode.lower()

    auto_interval = 3
    if st.session_state.caller_mode == "auto":
        with speed_col:
            auto_interval = st.slider("Call every (seconds)", 1, 10, 3)

    with reset_col:
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state.caller_pool    = fisher_yates_shuffle(st.session_state.items)
            st.session_state.caller_history = []
            st.session_state.caller_current = None
            st.session_state.auto_running   = False
            st.rerun()

    st.markdown("---")

    # ── Animated caller display ──────────────────────────────────────────────
    if current:
        display_html = f"""
        <div class="caller-wrapper">
          <div class="caller-inner">
            <span class="caller-number">{current}</span>
            <div class="caller-label">✨ Called! ✨</div>
            <div class="progress-bar-outer">
              <div class="progress-bar-inner" style="width:{pct}%;"></div>
            </div>
            <div style="color:rgba(255,255,255,0.85);font-size:1rem;
                        font-weight:700;margin-top:6px;">
              {called} / {total} called
            </div>
          </div>
        </div>"""
    else:
        display_html = """
        <div class="caller-wrapper">
          <div class="caller-inner">
            <div class="caller-idle">Press ▶ to start calling!</div>
          </div>
        </div>"""

    st.markdown(display_html, unsafe_allow_html=True)

    # ── Action buttons ───────────────────────────────────────────────────────
    all_done = len(remaining) == 0 and called > 0

    if st.session_state.caller_mode == "manual":
        btn_col, _ = st.columns([2, 5])
        with btn_col:
            if st.button(
                "▶ Next Item", type="primary",
                use_container_width=True,
                disabled=(len(remaining) == 0),
            ):
                pick = remaining[random.randint(0, len(remaining) - 1)]
                st.session_state.caller_current = pick
                st.session_state.caller_history.append(pick)
                st.rerun()

    else:
        # Auto mode: Start / Pause
        ac1, ac2, _ = st.columns([2, 2, 4])
        with ac1:
            if not st.session_state.auto_running:
                if st.button(
                    "▶ Start Auto", type="primary",
                    use_container_width=True,
                    disabled=(len(remaining) == 0),
                ):
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
                    '<span class="auto-indicator">● LIVE</span>',
                    unsafe_allow_html=True,
                )

    if all_done:
        st.success("🎉 All items have been called! Press **Reset All** to play again.")
        st.session_state.auto_running = False

    # ── Auto-advance ticker ───────────────────────────────────────────────────
    if st.session_state.auto_running and remaining:
        elapsed = time.time() - st.session_state.auto_last_tick
        if elapsed >= auto_interval:
            pick = remaining[random.randint(0, len(remaining) - 1)]
            st.session_state.caller_current = pick
            st.session_state.caller_history.append(pick)
            st.session_state.auto_last_tick = time.time()
            time.sleep(0.05)
            st.rerun()
        else:
            # Sleep until next tick (max 1 s to stay responsive to pause)
            time.sleep(min(auto_interval - elapsed, 1.0))
            st.rerun()

    # ── Call history ─────────────────────────────────────────────────────────
    if history:
        st.markdown("---\n**📜 Call History** (most recent first):")
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
