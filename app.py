import streamlit as st
import random
import io
from copy import deepcopy

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎉 Bingo Builder for Kids",
    page_icon="🎱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .main { background: #f0f4ff; }

    h1 { color: #5c35d9; text-align: center; font-size: 2.8rem !important; }
    h2 { color: #5c35d9; }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: #e8e0ff;
        border-radius: 16px;
        padding: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        color: #5c35d9;
        padding: 10px 24px;
    }
    .stTabs [aria-selected="true"] {
        background: #5c35d9 !important;
        color: white !important;
    }

    .bingo-card {
        background: white;
        border-radius: 20px;
        padding: 12px;
        margin: 8px;
        box-shadow: 0 4px 16px rgba(92,53,217,0.15);
        border: 3px solid #c9b8ff;
    }
    .bingo-title {
        text-align: center;
        font-weight: 900;
        font-size: 1.1rem;
        color: #5c35d9;
        margin-bottom: 8px;
        letter-spacing: 2px;
    }
    .bingo-cell {
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        font-weight: 700;
        text-align: center;
        word-break: break-word;
        border: 2px solid #e8e0ff;
        padding: 4px;
    }
    .free-cell {
        background: linear-gradient(135deg, #ffd6e7, #ffecb3) !important;
        border: 2px solid #ffb3c6 !important;
        color: #c0392b !important;
        font-size: 0.75rem !important;
    }

    .stButton > button {
        border-radius: 14px;
        font-weight: 700;
        font-size: 1rem;
        padding: 8px 20px;
        border: none;
        transition: all 0.2s;
    }
    .stButton > button:hover { transform: scale(1.04); }

    .template-btn > button {
        background: #e8f4fd !important;
        color: #1a73e8 !important;
        border: 2px solid #93c6f4 !important;
    }

    .caller-display {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 900;
        margin: 16px 0;
        box-shadow: 0 8px 32px rgba(102,126,234,0.4);
        animation: pop 0.3s ease;
    }
    @keyframes pop {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    .history-chip {
        display: inline-block;
        background: #e8e0ff;
        color: #5c35d9;
        border-radius: 20px;
        padding: 4px 12px;
        margin: 3px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .error-box {
        background: #ffe0e0;
        border: 2px solid #ffb3b3;
        border-radius: 12px;
        padding: 12px 18px;
        color: #c0392b;
        font-weight: 700;
    }

    .settings-box {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 12px rgba(92,53,217,0.1);
        border: 2px solid #e8e0ff;
    }
</style>
""", unsafe_allow_html=True)

# ─── Templates ─────────────────────────────────────────────────────────────────
TEMPLATES = {
    "Numbers 1–20": [str(i) for i in range(1, 21)],
    "Numbers 1–50": [str(i) for i in range(1, 51)],
    "Colors": ["Red","Blue","Green","Yellow","Orange","Purple","Pink","Brown",
               "Black","White","Gray","Cyan","Magenta","Lime","Indigo","Violet",
               "Gold","Silver","Beige","Teal","Maroon","Navy","Olive","Coral","Salmon"],
    "Basic Vocab": ["Apple","Ball","Cat","Dog","Egg","Fish","Girl","Hat","Ice","Jump",
                    "King","Lamp","Moon","Nest","Open","Play","Queen","Rain","Sun","Tree",
                    "Under","Van","Wind","Box","Year","Zoo","Ant","Bee","Cup","Door"],
}

# ─── Fisher-Yates Shuffle ───────────────────────────────────────────────────────
def fisher_yates_shuffle(lst):
    arr = list(lst)
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

# ─── Generate Cards ─────────────────────────────────────────────────────────────
def generate_cards(items, grid_size, num_cards, free_space):
    cards = []
    total_cells = grid_size * grid_size
    needed = total_cells - (1 if free_space else 0)

    if len(items) < needed:
        return None, f"❌ Not enough items! You need at least **{needed}** unique items for a {grid_size}×{grid_size} grid (you have {len(items)})."

    free_pos = (grid_size // 2) * grid_size + (grid_size // 2) if free_space else -1

    for _ in range(num_cards):
        shuffled = fisher_yates_shuffle(items)[:needed]
        card = []
        item_idx = 0
        for cell in range(total_cells):
            if cell == free_pos:
                card.append("⭐ FREE")
            else:
                card.append(shuffled[item_idx])
                item_idx += 1
        cards.append(card)

    return cards, None

# ─── Render Single Card as HTML ─────────────────────────────────────────────────
CELL_COLORS = [
    "#ffecd2","#d4f8e8","#dce8ff","#ffe8f4","#f3e8ff",
    "#fff9db","#e8fff3","#ffe8e8","#e8f4ff","#f9ffe8",
]

def render_card_html(card, grid_size, card_num):
    cell_size = max(40, min(80, 280 // grid_size))
    font_size = max(0.6, min(1.1, cell_size / 65))
    rows_html = ""
    for r in range(grid_size):
        row_html = "<tr>"
        for c in range(grid_size):
            idx = r * grid_size + c
            val = card[idx]
            color = CELL_COLORS[(r * grid_size + c) % len(CELL_COLORS)]
            extra_class = "free-cell" if val == "⭐ FREE" else ""
            if val != "⭐ FREE":
                style = f"background:{color};"
            else:
                style = "background:linear-gradient(135deg,#ffd6e7,#ffecb3);"
            row_html += (
                f'<td style="width:{cell_size}px;height:{cell_size}px;{style}'
                f'border-radius:10px;border:2px solid #e8e0ff;text-align:center;'
                f'vertical-align:middle;font-size:{font_size}rem;font-weight:700;'
                f'color:#333;padding:3px;word-break:break-word;" class="{extra_class}">'
                f'{val}</td>'
            )
        row_html += "</tr>"
        rows_html += row_html

    return f"""
    <div class="bingo-card">
        <div class="bingo-title">🎱 BINGO – Card #{card_num}</div>
        <table style="border-collapse:separate;border-spacing:4px;margin:auto;">
            {rows_html}
        </table>
    </div>
    """

# ─── PDF Generation ─────────────────────────────────────────────────────────────
def generate_pdf(cards, grid_size):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                 leftMargin=15*mm, rightMargin=15*mm,
                                 topMargin=15*mm, bottomMargin=15*mm)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('title', fontName='Helvetica-Bold',
                                      fontSize=14, textColor=colors.HexColor('#5c35d9'),
                                      alignment=1, spaceAfter=6)
        story = []
        cell_w = (A4[0] - 30*mm) / grid_size
        cell_h = min(cell_w, (A4[1] - 50*mm) / grid_size)

        pastel = [
            colors.HexColor('#ffecd2'), colors.HexColor('#d4f8e8'),
            colors.HexColor('#dce8ff'), colors.HexColor('#ffe8f4'),
            colors.HexColor('#f3e8ff'), colors.HexColor('#fff9db'),
            colors.HexColor('#e8fff3'), colors.HexColor('#ffe8e8'),
        ]

        for i, card in enumerate(cards):
            story.append(Paragraph(f"🎱 BINGO – Card #{i+1}", title_style))
            table_data = []
            for r in range(grid_size):
                row = []
                for c in range(grid_size):
                    val = card[r * grid_size + c]
                    row.append(Paragraph(val, ParagraphStyle('cell',
                        fontName='Helvetica-Bold', fontSize=max(7, 14 - grid_size),
                        alignment=1, leading=12)))
                table_data.append(row)

            col_widths = [cell_w] * grid_size
            row_heights = [cell_h] * grid_size
            t = Table(table_data, colWidths=col_widths, rowHeights=row_heights)

            ts = TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#c9b8ff')),
                ('ROUNDEDCORNERS', [8]),
                ('ROWBACKGROUNDS', (0,0), (-1,-1), pastel),
            ])
            # Color FREE cell
            for r in range(grid_size):
                for c in range(grid_size):
                    if card[r * grid_size + c] == "⭐ FREE":
                        ts.add('BACKGROUND', (c,r), (c,r), colors.HexColor('#ffd6e7'))
            t.setStyle(ts)
            story.append(t)
            story.append(Spacer(1, 6*mm))
            if i < len(cards) - 1 and (i + 1) % 2 == 0:
                story.append(PageBreak())
            elif i < len(cards) - 1:
                story.append(Spacer(1, 4*mm))

        doc.build(story)
        buf.seek(0)
        return buf.getvalue(), None
    except ImportError:
        return None, "reportlab not installed"

def generate_html_pdf(cards, grid_size):
    """Fallback: generate printable HTML."""
    pastel = ["#ffecd2","#d4f8e8","#dce8ff","#ffe8f4","#f3e8ff","#fff9db"]
    cards_html = ""
    for i, card in enumerate(cards):
        cell_size = max(50, min(90, 400 // grid_size))
        font_size = max(10, min(18, cell_size // 4))
        rows = ""
        for r in range(grid_size):
            rows += "<tr>"
            for c in range(grid_size):
                val = card[r * grid_size + c]
                color = "#ffd6e7" if val == "⭐ FREE" else pastel[(r*grid_size+c) % len(pastel)]
                rows += f'<td style="width:{cell_size}px;height:{cell_size}px;background:{color};border:2px solid #c9b8ff;border-radius:8px;text-align:center;vertical-align:middle;font-size:{font_size}px;font-weight:700;word-break:break-word;">{val}</td>'
            rows += "</tr>"
        if i > 0 and i % 2 == 0:
            cards_html += '<div style="page-break-before:always;"></div>'
        cards_html += f"""
        <div style="display:inline-block;margin:16px;vertical-align:top;">
            <div style="font-family:Arial,sans-serif;font-weight:900;font-size:18px;color:#5c35d9;text-align:center;margin-bottom:8px;">🎱 BINGO – Card #{i+1}</div>
            <table style="border-collapse:separate;border-spacing:4px;">{rows}</table>
        </div>"""

    return f"""<!DOCTYPE html>
<html><head><title>Bingo Cards</title>
<style>
  body {{ font-family: Arial, sans-serif; background: white; }}
  @media print {{ button {{ display: none; }} }}
</style></head>
<body>
<div style="text-align:center;margin-bottom:16px;">
  <button onclick="window.print()" style="background:#5c35d9;color:white;border:none;border-radius:12px;padding:10px 24px;font-size:16px;font-weight:700;cursor:pointer;">🖨️ Print Cards</button>
</div>
{cards_html}
</body></html>"""

# ─── Session State Init ─────────────────────────────────────────────────────────
for key, default in [
    ("cards", None),
    ("items", []),
    ("words_input", ""),
    ("caller_pool", []),
    ("caller_history", []),
    ("caller_current", None),
    ("error_msg", None),
    ("active_tab", 0),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1>🎉 Bingo Builder for Kids</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#888;font-size:1.1rem;'>Create fun bingo cards for your classroom in seconds!</p>", unsafe_allow_html=True)

# ─── Tabs ───────────────────────────────────────────────────────────────────────
tab_words, tab_numbers = st.tabs(["🔤 Words Mode", "🔢 Numbers Mode"])

with tab_words:
    if st.session_state.active_tab != 0:
        st.session_state.error_msg = None
        st.session_state.active_tab = 0

    st.markdown("### Quick Templates")
    t_cols = st.columns(4)
    for idx, (label, vals) in enumerate(TEMPLATES.items()):
        with t_cols[idx]:
            with st.container():
                st.markdown('<div class="template-btn">', unsafe_allow_html=True)
                if st.button(f"📋 {label}", key=f"tpl_{idx}"):
                    st.session_state.words_input = ", ".join(vals)
                    st.session_state.error_msg = None
                st.markdown('</div>', unsafe_allow_html=True)

    words_raw = st.text_area(
        "Enter your words (comma or newline separated):",
        value=st.session_state.words_input,
        height=150,
        placeholder="apple, banana, cat, dog...\nor one per line",
        key="words_textarea"
    )
    st.session_state.words_input = words_raw

    # Parse words
    raw_items = [w.strip() for part in words_raw.replace("\n", ",").split(",") for w in [part.strip()] if w]
    words_items = list(dict.fromkeys(filter(None, raw_items)))
    st.caption(f"✅ {len(words_items)} unique words detected")
    current_items = words_items
    mode = "words"

with tab_numbers:
    if st.session_state.active_tab != 1:
        st.session_state.error_msg = None
        st.session_state.active_tab = 1

    nc1, nc2 = st.columns(2)
    with nc1:
        num_start = st.number_input("Start number:", value=1, min_value=0, max_value=9999, key="num_start")
    with nc2:
        num_end = st.number_input("End number:", value=50, min_value=1, max_value=9999, key="num_end")

    if num_end > num_start:
        num_items = [str(i) for i in range(int(num_start), int(num_end) + 1)]
        st.caption(f"✅ {len(num_items)} numbers ({int(num_start)}–{int(num_end)})")
    else:
        num_items = []
        st.warning("End must be greater than Start.")
    current_items = num_items
    mode = "numbers"

# We need to pick items based on which tab is active
# Use a workaround with a radio hidden selector
st.markdown("---")

# ─── Settings ───────────────────────────────────────────────────────────────────
st.markdown("### ⚙️ Bingo Settings")
st.markdown('<div class="settings-box">', unsafe_allow_html=True)

scol1, scol2, scol3 = st.columns(3)
with scol1:
    grid_size = st.selectbox("Grid Size:", [3, 4, 5, 6, 7, 8],
                              index=2, format_func=lambda x: f"{x}×{x}")
with scol2:
    num_cards = st.slider("Number of Cards:", min_value=10, max_value=15, value=10)
with scol3:
    if grid_size >= 5:
        free_space = st.toggle("⭐ FREE SPACE (center)", value=True)
    else:
        free_space = False
        st.info("FREE SPACE available for 5×5+")

st.markdown('</div>', unsafe_allow_html=True)

# ─── Determine Active Items ─────────────────────────────────────────────────────
# We use a mode selector since tabs run in parallel
mode_sel = st.radio("Select input mode:", ["🔤 Words Mode", "🔢 Numbers Mode"],
                     horizontal=True, label_visibility="collapsed")
if "Words" in mode_sel:
    active_items = words_items
else:
    active_items = num_items

# ─── Generate Button ────────────────────────────────────────────────────────────
gen_col, _ = st.columns([2, 5])
with gen_col:
    if st.button("🎲 Generate Bingo Cards!", type="primary", use_container_width=True):
        st.session_state.error_msg = None
        cards, err = generate_cards(active_items, grid_size, num_cards, free_space)
        if err:
            st.session_state.error_msg = err
            st.session_state.cards = None
        else:
            st.session_state.cards = cards
            st.session_state.items = active_items
            st.session_state.caller_pool = fisher_yates_shuffle(active_items)
            st.session_state.caller_history = []
            st.session_state.caller_current = None

if st.session_state.error_msg:
    st.markdown(f'<div class="error-box">{st.session_state.error_msg}</div>', unsafe_allow_html=True)

# ─── Display Cards ──────────────────────────────────────────────────────────────
if st.session_state.cards:
    cards = st.session_state.cards
    st.markdown(f"---\n### 🃏 Your {len(cards)} Bingo Cards")

    cols_per_row = 2 if grid_size <= 5 else 1
    for row_start in range(0, len(cards), cols_per_row):
        cols = st.columns(cols_per_row)
        for ci, card_idx in enumerate(range(row_start, min(row_start + cols_per_row, len(cards)))):
            with cols[ci]:
                st.markdown(render_card_html(cards[card_idx], grid_size, card_idx + 1),
                            unsafe_allow_html=True)

    # ─── Download PDF ───────────────────────────────────────────────────────────
    st.markdown("---\n### 💾 Download")
    dl1, dl2 = st.columns(2)

    with dl1:
        pdf_bytes, err = generate_pdf(cards, grid_size)
        if pdf_bytes:
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name="bingo_cards.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            # Fallback to HTML
            html_content = generate_html_pdf(cards, grid_size)
            st.download_button(
                label="📥 Download Printable HTML",
                data=html_content.encode(),
                file_name="bingo_cards.html",
                mime="text/html",
                use_container_width=True,
            )
            if err:
                st.caption(f"(PDF unavailable: {err} — HTML provided instead)")

    with dl2:
        html_content = generate_html_pdf(cards, grid_size)
        st.download_button(
            label="🖨️ Download Printable HTML",
            data=html_content.encode(),
            file_name="bingo_cards.html",
            mime="text/html",
            use_container_width=True,
        )

    # ─── Play Caller ────────────────────────────────────────────────────────────
    st.markdown("---\n### 🎡 Play Caller")

    pool = st.session_state.caller_pool
    history = st.session_state.caller_history
    remaining = [x for x in pool if x not in history]

    cal1, cal2, cal3 = st.columns([2, 2, 3])
    with cal1:
        if st.button("🎡 Call Next Item!", use_container_width=True, disabled=len(remaining) == 0):
            if remaining:
                pick = remaining[random.randint(0, len(remaining) - 1)]
                st.session_state.caller_current = pick
                st.session_state.caller_history.append(pick)
    with cal2:
        if st.button("🔄 Reset Caller", use_container_width=True):
            st.session_state.caller_pool = fisher_yates_shuffle(st.session_state.items)
            st.session_state.caller_history = []
            st.session_state.caller_current = None

    with cal3:
        total = len(pool)
        called = len(history)
        st.metric("Progress", f"{called} / {total}", delta=f"{total - called} remaining")

    if st.session_state.caller_current:
        st.markdown(
            f'<div class="caller-display">🎱 {st.session_state.caller_current}</div>',
            unsafe_allow_html=True,
        )
    elif len(remaining) == 0 and history:
        st.success("🎉 All items have been called! Reset to play again.")

    if history:
        st.markdown("**📜 Call History:**")
        chips = " ".join(f'<span class="history-chip">{item}</span>' for item in history)
        st.markdown(chips, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#aaa;font-size:0.85rem;'>🎉 Bingo Builder for Kids – Made with ❤️ using Streamlit</p>",
    unsafe_allow_html=True,
)
