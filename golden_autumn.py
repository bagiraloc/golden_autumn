import streamlit as st
import pandas as pd
import time

# 🔸 Налаштування сторінки
st.set_page_config(page_title="Золота Осінь 2025", page_icon="🍁", layout="wide")

# 🔸 Темна тема і стилі
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

# 🔸 Анімація листя
st.markdown("""
    <div style="text-align:center; font-size:48px; animation: fall 3s infinite alternate;">
        🍁 🍂 🍁
    </div>
    <style>
    @keyframes fall {
      0% {opacity: 0.5; transform: translateY(0px);}
      100% {opacity: 1; transform: translateY(20px);}
    }
    </style>
""", unsafe_allow_html=True)

# 🔸 Заголовок
st.markdown("<h1>👑 Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)

# 🔸 Посилання на таблицю (твоє!)
sheet_id = "1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY"
sheet_name = "Аркуш1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# 🔸 Автооновлення кожні 5 секунд
placeholder = st.empty()
refresh_interval = 5

while True:
    try:
        df = pd.read_csv(url)
        if not df.empty:
            df = df.dropna(how="all")
            # 👑 Додаємо корону першому місцю
            if "Місце" in df.columns and "Ім'я" in df.columns and not df.empty:
                df = df.sort_values(by=["Місце"])
                df.iloc[0, df.columns.get_loc("Ім'я")] = "👑 " + str(df.iloc[0]["Ім'я"])
            placeholder.dataframe(df, use_container_width=True, hide_index=True)
        else:
            placeholder.info("🕊 Дані ще не додані до таблиці.")
    except Exception as e:
        placeholder.error("❌ Помилка зчитування Google Sheets. Перевір посилання або доступ.")
    time.sleep(refresh_interval)
