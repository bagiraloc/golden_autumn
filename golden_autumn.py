import streamlit as st
import pandas as pd
import random
import time
from streamlit_gsheets import GSheetsConnection

# ------------------ Налаштування сторінки ------------------
st.set_page_config(page_title="Золота Осінь 2025", page_icon="🍁", layout="wide")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit?gid=0"

# ------------------ Темна тема і анімації ------------------
st.markdown("""
<style>
:root{
  --gold:#f6c453;
  --gold-strong:#ffd700;
  --bg:#0b0d10;
  --panel:#121416;
  --muted:#e0e0e0;
}
html, body, .stApp {
  background: linear-gradient(180deg, var(--bg), #0f1113) !important;
  color: var(--muted) !important;
}
.title {
  text-align:center;
  font-size:36px;
  color:var(--gold);
  font-weight:700;
  text-shadow: 0 0 18px rgba(246,196,83,0.3);
  margin: 8px 0 18px 0;
}
.leaf {
  position: fixed;
  top: -8vh;
  font-size: 28px;
  color: var(--gold-strong);
  opacity: 0.95;
  animation-name: fall;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  z-index: 0;
  pointer-events: none;
}
@keyframes fall {
  0% { transform: translateY(-5vh) rotate(0deg); opacity: 1; }
  100% { transform: translateY(120vh) rotate(360deg); opacity: 0.25; }
}
.results-wrap { width:100%; overflow:auto; }
table.results {
  width:100%;
  border-collapse: collapse;
  background: rgba(18,20,22,0.85);
  color: var(--muted);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.6);
  overflow: hidden;
  font-size:16px;
}
table.results th, table.results td {
  padding: 10px 12px;
  text-align: center;
  border-bottom: 1px solid rgba(246,196,83,0.08);
}
table.results th {
  background: rgba(20,22,24,0.9);
  color: var(--gold);
  font-weight:600;
}
.crown {
  display:inline-block;
  animation: crownPulse 3s ease-in-out infinite;
  color: var(--gold-strong);
  text-shadow: 0 0 8px rgba(255,215,0,0.6);
}
@keyframes crownPulse {
  0% { transform: scale(1); filter: drop-shadow(0 0 6px rgba(255,215,0,0.3)); }
  50% { transform: scale(1.08); filter: drop-shadow(0 0 20px rgba(255,215,0,0.7)); }
  100% { transform: scale(1); filter: drop-shadow(0 0 6px rgba(255,215,0,0.3)); }
}
tr.new-row {
  animation: slideUpFromBottom 0.9s cubic-bezier(.2,.9,.3,1) both;
  background: linear-gradient(90deg, rgba(255,215,0,0.06), rgba(255,215,0,0.01));
}
@keyframes slideUpFromBottom {
  0% { transform: translateY(60px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}
table.results tbody tr:hover { background: rgba(246,196,83,0.03); }
</style>
""", unsafe_allow_html=True)

# ------------------ Функція анімації листя ------------------
def render_leaves(count: int = 18):
    html = ""
    for i in range(count):
        left = random.randint(0, 95)
        duration = round(random.uniform(8, 16), 2)
        delay = round(random.uniform(0, 10), 2)
        size = random.randint(22, 42)
        html += f'<div class="leaf" style="left:{left}%; animation-duration:{duration}s; animation-delay:{delay}s; font-size:{size}px;">🍁</div>'
    st.markdown(html, unsafe_allow_html=True)

render_leaves(18)

st.markdown('<div class="title">Золота Осінь 2025</div>', unsafe_allow_html=True)

# ------------------ З'єднання з Google Sheets ------------------
conn = st.connection("gsheets", type=GSheetsConnection)

# ------------------ Основна функція ------------------
def load_data():
    df = conn.read(spreadsheet=SHEET_URL)
    df = pd.DataFrame(df)
    expected_cols = ["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"]
    for c in expected_cols:
        if c not in df.columns:
            df[c] = pd.NA
    df = df[expected_cols]
    df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce").fillna(0.0)
    df = df.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
    df["Місце"] = df.index + 1
    return df

# ------------------ Автоматичне оновлення ------------------
st_autorefresh = st.empty()
st_autorefresh.text("⏳ Оновлення даних кожні 5 секунд...")

# ------------------ Відображення таблиці ------------------
placeholder = st.empty()

while True:
    # ------------------ Автоматичне оновлення ------------------
from streamlit_autorefresh import st_autorefresh

# Автоматичне оновлення кожні 10 секунд
st_autorefresh(interval=10 * 1000, key="data_refresh")

# ------------------ Завантаження даних ------------------
df = load_data()

# ------------------ Відображення таблиці ------------------
rows_html = ""
for i, row in df.iterrows():
    place = int(row["Місце"])
    name = row["Ім’я"] or ""
    club = row["Клуб"] or ""
    vid = row["Вид"] or ""
    score = row["Оцінка"]

    if place == 1:
        name_html = f"<span class='crown'>👑 {name}</span>"
    else:
        name_html = name

    rows_html += f"<tr><td>{place}</td><td>{name_html}</td><td>{club}</td><td>{vid}</td><td>{score:.3f}</td></tr>"

html = f"""
<div class='results-wrap'>
  <table class='results'>
    <thead><tr><th>Місце</th><th>Ім’я</th><th>Клуб</th><th>Вид</th><th>Оцінка</th></tr></thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>
"""
st.markdown(html, unsafe_allow_html=True)
