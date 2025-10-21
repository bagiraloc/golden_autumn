import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection
from streamlit_autorefresh import st_autorefresh

# -------------------- Налаштування сторінки --------------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# -------------------- CSS стиль --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #0d0d0d, #1a1a1a);
    color: #f6c453;
    overflow-x: hidden;
}
h1 {
    text-align: center;
    color: #f6c453;
    font-weight: bold;
    text-shadow: 0 0 25px #f6c453;
    margin-bottom: 30px;
    animation: glow 2s ease-in-out infinite alternate;
}
@keyframes glow {
    from { text-shadow: 0 0 15px #f6c453; }
    to { text-shadow: 0 0 35px #ffd700; }
}
table {
    width: 100%;
    border-collapse: collapse;
    background: rgba(30,30,30,0.9);
    color: #f6c453;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(246,196,83,0.3);
}
th, td {
    padding: 10px;
    text-align: center;
    font-size: 18px;
}
th {
    background-color: #333;
    color: #f6c453;
    border-bottom: 2px solid #f6c453;
}
tr {
    transition: transform 0.4s ease, opacity 0.4s ease;
}
tr.new {
    transform: translateY(40px);
    opacity: 0;
    animation: slideUp 0.7s forwards;
}
@keyframes slideUp {
    from { transform: translateY(40px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
.crown {
    animation: crownPulse 2.5s ease-in-out infinite;
}
@keyframes crownPulse {
    0%, 100% { text-shadow: 0 0 10px #ffd700; }
    50% { text-shadow: 0 0 25px #ffea00; }
}
.leaf {
    position: fixed;
    top: -10vh;
    color: #f6c453;
    opacity: 0.8;
    animation: fall linear infinite;
    z-index: -1;
}
@keyframes fall {
    0% { transform: translateY(0) rotate(0deg); }
    100% { transform: translateY(110vh) rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# -------------------- Анімація листочків 🍁 --------------------
leaves_html = ""
for i in range(25):
    left = random.randint(0, 100)
    duration = random.uniform(15, 30)
    delay = random.uniform(0, 20)
    size = random.uniform(20, 36)
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s; font-size:{size}px;">🍁</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

# -------------------- Назва --------------------
st.markdown("<h1>Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)

# -------------------- Оновлення сторінки кожні 10 сек --------------------
st_autorefresh(interval=10 * 1000, key="data_refresh")

# -------------------- З'єднання з Google Sheets --------------------
conn = st.connection("gsheets", type=GSheetsConnection)

sheet_url = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit?gid=0"

@st.cache_data(ttl=10)
def load_data():
    try:
        df = conn.read(spreadsheet=sheet_url)
        if not df.empty:
            df = df.dropna(how="all")
            df.columns = [c.strip() for c in df.columns]
            df = df[df["Ім’я"].notna()]
            df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")
            df = df.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
            df["Місце"] = df.index + 1
        else:
            df = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
    except Exception as e:
        st.error(f"❌ Помилка читання Google Sheets: {e}")
        df = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
    return df

df = load_data()

# -------------------- Відображення таблиці --------------------
if not df.empty:
    rows_html = ""
    for i, row in df.iterrows():
        place = int(row["Місце"])
        name = str(row["Ім’я"])
        club = str(row["Клуб"])
        vid = str(row["Вид"])
        score = row["Оцінка"]

        if place == 1:
            name_html = f"<span class='crown'>👑 {name}</span>"
        else:
            name_html = name

        rows_html += f"<tr class='new'><td>{place}</td><td>{name_html}</td><td>{club}</td><td>{vid}</td><td>{score:.3f}</td></tr>"

    html = f"""
    <div class='results-wrap'>
      <table class='results'>
        <thead><tr><th>Місце</th><th>Ім’я</th><th>Клуб</th><th>Вид</th><th>Оцінка</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
