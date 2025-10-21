import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

# 🌙 Темна тема + базова конфігурація
st.set_page_config(
    page_title="Golden Autumn 🍂",
    page_icon="🍁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS для темного стилю + анімація листочків
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 2.2em;
        color: #ffb347;
        margin-bottom: 20px;
        text-shadow: 0 0 10px #ffb34780;
    }
    .leaf {
        position: fixed;
        top: -50px;
        font-size: 24px;
        animation-name: fall;
        animation-timing-function: linear;
        animation-iteration-count: infinite;
    }
    @keyframes fall {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(120vh) rotate(360deg); opacity: 0.2; }
    }
    </style>
""", unsafe_allow_html=True)

# 🍁 Анімація листочків
def falling_leaves():
    leaves = ["🍂", "🍁", "🍃"]
    html = ""
    for i in range(20):
        leaf = random.choice(leaves)
        left = random.randint(0, 100)
        duration = random.uniform(6, 12)
        delay = random.uniform(0, 5)
        html += f'<div class="leaf" style="left: {left}%; animation-duration: {duration}s; animation-delay: {delay}s;">{leaf}</div>'
    st.markdown(html, unsafe_allow_html=True)

falling_leaves()

# 🧾 Підключення до Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Учасниці", usecols=list(range(3)), ttl=5)
    df = df.dropna(how="all")
except Exception as e:
    st.error("❌ Помилка при з'єднанні з Google Sheets")
    st.stop()

# 🌟 Заголовок
st.markdown('<div class="title">Golden Autumn 🍁</div>', unsafe_allow_html=True)

# 📋 Форма для додавання учасниці
with st.form("add_participant", clear_on_submit=True):
    name = st.text_input("Ім’я та прізвище", placeholder="Введіть ім’я...")
    age = st.number_input("Вік", min_value=5, max_value=100, step=1)
    city = st.text_input("Місто", placeholder="Звідки учасниця?")
    submitted = st.form_submit_button("Додати 🌟")

    if submitted:
        if name and city:
            new_row = pd.DataFrame([[name, age, city]], columns=["Ім’я", "Вік", "Місто"])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(worksheet="Учасниці", data=updated_df)
            st.success(f"✅ Учасницю **{name}** успішно додано!")
            st.balloons()
        else:
            st.warning("⚠️ Заповніть усі поля!")

# 🧡 Таблиця учасниць
st.markdown("### Учасниці:")
st.dataframe(df, use_container_width=True, hide_index=True)
