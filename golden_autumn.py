# golden_autumn.py
import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection
from streamlit_autorefresh import st_autorefresh
import html

# ---------------- Page config ----------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# ---------------- Auto-refresh every 5 seconds ----------------
st_autorefresh(interval=5000, key="autorefresh_counter")

# ---------------- Styles (dark + crown + leaf + row animation) ----------------
st.markdown(
    """
    <style>
    body { background: radial-gradient(circle at top, #0d0d0d 0%, #000000 100%); color:#f6c453; }
    h1 { text-align:center; color:#f6c453; font-weight:700; text-shadow:0 0 18px #f6c453; }
    .crown { text-shadow: 0 0 12px #ffd700; font-weight:700; }
    table.custom { width:100%; border-collapse:collapse; margin-top:18px; background: rgba(18,18,18,0.95); border-radius:12px; overflow:hidden; box-shadow: 0 0 24px rgba(246,196,83,0.18); }
    table.custom th, table.custom td { padding:12px 14px; text-align:center; font-size:18px; color:#f6c453; }
    table.custom th { background:#151515; border-bottom:2px solid #f6c453; }
    tr.new-row { animation: slideUp 0.7s ease-out; }
    @keyframes slideUp { from { transform: translateY(30px); opacity:0; } to { transform: translateY(0); opacity:1; } }

    /* leaf image uses small maple icon (remote) - fixed size and fall animation */
    .leaf {
      position: fixed;
      width: 40px;
      height: 40px;
      background-image: url('https://upload.wikimedia.org/wikipedia/commons/0/06/RedMapleLeaf.png');
      background-size: contain;
      background-repeat: no-repeat;
      pointer-events: none;
      z-index: 1;
      animation: fall linear infinite;
    }
    @keyframes fall {
      0% { transform: translateY(-10vh) rotate(0deg); opacity:1; }
      100% { transform: translateY(110vh) rotate(360deg); opacity:0; }
    }

    /* small responsiveness */
    @media (max-width:800px) {
      table.custom th, table.custom td { font-size:16px; padding:10px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Title ----------------
st.markdown("<h1>👑 Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)

# ---------------- Decorative maple leaves (klenovi) ----------------
for i in range(10):
    left = random.randint(0, 95)
    dur = round(random.uniform(6, 14), 2)
    delay = round(random.uniform(0, 6), 2)
    size = random.randint(28, 48)
    st.markdown(
        f"""
        <div class="leaf" style="
            left:{left}%;
            width:{size}px; height:{size}px;
            animation-duration:{dur}s;
            animation-delay:{delay}s;
        "></div>
        """,
        unsafe_allow_html=True,
    )

# ---------------- Read Google Sheet ----------------
# Replace with your Google Sheet URL (the one you sent earlier)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit#gid=0"

df = None
error_text = None

try:
    # Use streamlit connections API for gSheets (streamlit_gsheets)
    conn = st.connection("gsheets", type=GSheetsConnection)
    # IMPORTANT: do NOT pass non-ascii worksheet name (avoid 'Аркуш1' param). Just pass spreadsheet URL.
    df = conn.read(spreadsheet=SHEET_URL)
    # The library sometimes returns a dict-like; ensure it's a DataFrame
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    # Drop completely empty rows
    df = df.dropna(how="all").copy()

    # If columns are present but have weird names, try to standardize common headers
    # Expecting columns like: ["Місце","Ім’я","Клуб","Вид","Оцінка"]
    # If Google sheet has different header row, user can adjust sheet accordingly.
    if df.empty:
        pass  # nothing to show
    else:
        # Ensure text values are strings (avoid encoding problems)
        df = df.astype(object).where(pd.notnull(df), "")
        # Keep original order from the sheet (do not sort automatically)
        # Mark first visible row as first place (for crown) — we'll add crown to first name cell.
except Exception as e:
    df = None
    error_text = str(e)

# ---------------- Error handling ----------------
if error_text:
    st.error("❌ Помилка при з'єднанні з Google Sheets")
    st.caption(error_text)

# ---------------- Render table (custom HTML so we can inject crown and animation) ----------------
if isinstance(df, pd.DataFrame) and not df.empty:
    # Determine column names to display (use df.columns as-is)
    cols = list(df.columns)

    # Build header row HTML
    header_html = "<thead><tr>"
    for c in cols:
        header_html += f"<th>{html.escape(str(c))}</th>"
    header_html += "</tr></thead>"

    # Build body rows
    body_html = "<tbody>"
    for i, row in df.iterrows():
        # Add animation class only for the last row in sheet (so newly added row appears animated on refresh)
        css_cls = "new-row" if i == len(df) - 1 else ""
        body_html += f"<tr class='{css_cls}'>"
        for j, col in enumerate(cols):
            cell = row[col]
            cell_str = "" if cell is None else str(cell)
            # Add crown to the first visible row's name column if column name contains "Ім" or "name"
            if i == 0 and ("ім" in col.lower() or "name" in col.lower() or "ім'я" in col.lower()):
                # keep crown + styled span
                body_html += f"<td><span class='crown'>👑 {html.escape(cell_str)}</span></td>"
            else:
                body_html += f"<td>{html.escape(cell_str)}</td>"
        body_html += "</tr>"
    body_html += "</tbody>"

    table_html = f"<table class='custom'>{header_html}{body_html}</table>"

    st.markdown(table_html, unsafe_allow_html=True)
# If sheet empty — show nothing (you asked to remove "no participants" string)
