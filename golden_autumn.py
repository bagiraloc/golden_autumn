import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

# ---------- Налаштування сторінки ----------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# ---------- Підключення до Google Sheets ----------
conn = st.connection("gsheets", type=GSheetsConnection)

# Встав твоє посилання сюди:
sheet_url = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit?gid=0"

# Спроба зчитати існуючу таблицю
try:
    df = conn.read(spreadsheet=sheet_url, usecols=list(range(5)))
except Exception:
    df = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])

# ---------- Стилі та анімації ----------
st.markdown("""
<style>
.stApp, .css-1dp5vir {
  background-color: #0d0d0d !important;
  color: #f6c453 !important;
}
h1 {
  text-align:center;
  color:#f6c453;
  text-shadow:0 0 20px #f6c453;
  animation: glow 2s infinite alternate;
}
@keyframes glow {
  from { text-shadow: 0 0 10px #f6c453; }
  to { text-shadow: 0 0 35px #ffd700; }
}
.leaf {
  position: fixed;
  top: -12vh;
  color: #ffd54f;
  font-size: 28px;
  opacity: 0.9;
  animation: fall linear infinite;
  z-index: 0;
}
@keyframes fall {
  0% { transform: translateY(-10vh) rotate(0deg); }
  100% { transform: translateY(120vh) rotate(360deg); }
}
.table-wrap { width:100%; overflow:auto; }
.results-table {
  width:100%;
  border-collapse: collapse;
  background: rgba(25,25,25,0.95);
  color:#f6c453;
  box-shadow: 0 8px 30px rgba(0,0,0,0.6);
  border-radius:12px;
}
.results-table th, .results-table td {
  padding:10px; text-align:center;
  border-bottom:1px solid rgba(246,196,83,0.08);
}
.results-table th {
  background:#151515; color:#f6c453; font-weight:600;
}
.row-new {
  animation: slideUp 0.9s ease-out;
  background: rgba(246,196,83,0.05);
}
@keyframes slideUp {
  from { transform: translateY(40px); opacity: 0; }
  to   { transform: translateY(0); opacity: 1; }
}
tr.first-place {
  animation: goldPulse 2s ease-in-out infinite;
}
@keyframes goldPulse {
  0%,100% { box-shadow: 0 0 10px rgba(255,215,0,0.3); }
  50%    { box-shadow: 0 0 30px rgba(255,215,0,0.7); }
}
.stButton>button {
  background: linear-gradient(90deg, #f6c453, #b8860b);
  color:#0d0d0d !important;
  border:none; border-radius:8px; padding:8px 14px;
}
.stButton>button:hover {
  background: linear-gradient(90deg, #ffd700, #f6c453);
}
</style>
""", unsafe_allow_html=True)

# ---------- Листочки ----------
leaves_html = ""
for i in range(28):
    left = random.randint(0, 100)
    duration = random.uniform(16, 30)
    delay = random.uniform(0, 20)
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s;">🍁</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

st.markdown("<h1>Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)

# ---------- Панель судді ----------
with st.expander("Панель судді", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    name = c1.text_input("Прізвище")
    club = c2.text_input("Клуб")
    event = c3.text_input("Вид")
    score = c4.text_input("Оцінка (напр. 27.750)")
    colA, colB = st.columns([1,1])
    add_btn = colA.button("➕ Додати учасницю")
    clear_btn = colB.button("🧹 Очистити таблицю")

# ---------- Додавання / очищення ----------
if add_btn and name and club and event and score:
    try:
        val = float(score.replace(",", "."))
        new = pd.DataFrame([[None, name, club, event, val]], columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
        df = pd.concat([df, new], ignore_index=True)
        df["Оцінка"] = df["Оцінка"].astype(float)
        df = df.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
        df["Місце"] = df.index + 1
        conn.update(spreadsheet=sheet_url, data=df)
        st.success("✅ Учасницю додано!")
    except ValueError:
        st.error("⚠️ Неправильний формат оцінки!")

if clear_btn:
    blank = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
    conn.update(spreadsheet=sheet_url, data=blank)

# ---------- Відображення ----------
if not df.empty:
    df["Оцінка"] = df["Оцінка"].map(lambda x: f"{x:.3f}")
    df.loc[0, "Ім’я"] = f"👑 {df.loc[0, 'Ім’я']}"
    rows = ""
    for _, r in df.iterrows():
        cls = "first-place" if r["Місце"] == 1 else ""
        rows += (f"<tr class='{cls}'>"
                 + "".join([f"<td>{val}</td>" for val in r.values])
                 + "</tr>")
    table_html = ("<div class='table-wrap'><table class='results-table'><thead><tr>"
                  + "".join([f"<th>{c}</th>" for c in df.columns])
                  + "</tr></thead><tbody>"
                  + rows + "</tbody></table></div>")
    st.markdown(table_html, unsafe_allow_html=True)
