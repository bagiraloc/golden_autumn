import streamlit as st
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection

# Заголовок сторінки
st.set_page_config(page_title="Золота Осінь 2025", page_icon="🍁", layout="wide")

# Темна тема + стилі
st.markdown("""
    <style>
        body {background-color: #0e1117; color: #ffffff;}
        .main {background-color: #0e1117;}
        h1 {color: #ffcc00; text-align: center; font-size: 48px;}
        table {border-radius: 10px; overflow: hidden;}
        th, td {text-align: center !important;}
        .stDataFrame {background-color: #1e232b; color: #fff;}
    </style>
""", unsafe_allow_html=True)

# Анімація листя 🍁
st.markdown("""
    <div style="text-align:center; font-size:48px; animation: fall 3s infinite alternate;">
        🍂 🍁 🍂
    </div>
    <style>
    @keyframes fall {
      0% {opacity: 0.4; transform: translateY(0px);}
      100% {opacity: 1; transform: translateY(20px);}
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>👑 Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)

# Підключення до Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit?gid=0"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("❌ Помилка при з'єднанні з Google Sheets")
    st.stop()

# Автооновлення таблиці
REFRESH_INTERVAL = 5  # секунд

placeholder = st.empty()

while True:
    try:
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Аркуш1")
        if df is not None and not df.empty:
            df = df.dropna(how="all")
            # Додаємо корону лідеру (1 місце)
            if "Місце" in df.columns and not df.empty:
                df = df.sort_values(by=["Місце"])
                df.iloc[0, df.columns.get_loc("Ім'я")] = "👑 " + str(df.iloc[0]["Ім'я"])
            placeholder.dataframe(df, use_container_width=True, hide_index=True)
        else:
            placeholder.info("Дані ще не додані в таблицю.")
    except Exception as e:
        placeholder.error("❌ Помилка при з'єднанні з Google Sheets")
    time.sleep(REFRESH_INTERVAL)
