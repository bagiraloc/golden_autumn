import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from streamlit_autorefresh import st_autorefresh
import random

# -------------------- Налаштування сторінки --------------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# -------------------- Автооновлення кожні 5 секунд --------------------
st_autorefresh(interval=5000, key="data_refresh")

# -------------------- Темна тема та стилі --------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0d0d0d 0%, #000000 100%);
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
    background: rgba(20,20,20,0.95);
    color: #f6c453;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 0 25px rgba(246,196,83,0.3);
}
th, td {
    padding: 12px;
    text-align: center;
    font-size: 18px;
}
th {
    background-color: #111;
    color: #f6c453;
    border-bottom: 2px solid #f6c453;
}
tr {
    transition: transform 0.4s ease, opacity 0.4s ease;
}
tr.new {
    transform: translateY(40px);
    opacity: 0;
    animation: slideUp 0.8s forwards;
}
@keyframes slideUp {
    from { transform: translateY(40px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* Анімація листочків */
.leaf {
    position: fixed;
    width: 40px;
    height: 40px;
    background-image: url('https://cdn-icons-png.flaticon.com/512/415/415733.png');
    background-size: cover;
    animation: fall linear infinite;
}
@keyframes fall {
    0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
    100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# -------------------- Заголовок --------------------
st.markdown("<h1>👑 Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)

# -------------------- З’єднання з Google Sheets --------------------
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Аркуш1")
    df = df.dropna(how="all")

    # Показ таблиці
    st.markdown("### Результати турніру")
    st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("❌ Помилка при з'єднанні з Google Sheets")
    st.write(e)

# -------------------- Декоративні листочки 🍁 --------------------
leaf_count = 15
for i in range(leaf_count):
    st.markdown(
        f"""
        <div class="leaf" style="
            left:{random.randint(0,100)}%;
            animation-duration:{random.uniform(5,10)}s;
            animation-delay:{random.uniform(0,5)}s;
        "></div>
        """, unsafe_allow_html=True
    )
