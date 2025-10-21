import streamlit as st
import pandas as pd
import time
import random
from streamlit_gsheets import GSheetsConnection

# 🌑 Настройки страницы
st.set_page_config(page_title="Золота Осінь 2025", page_icon="👑", layout="centered")

# 👑 Заголовок
st.markdown("""
    <h1 style='text-align:center; color:gold;'>
        👑 Золота Осінь 2025 🍁
    </h1>
""", unsafe_allow_html=True)

# 🌿 CSS — анимация листьев и стиль таблицы
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }

    /* 🍁 Падающие листья */
    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
    }

    .leaf {
        position: fixed;
        top: 0;
        font-size: 2rem;
        animation: fall linear infinite;
        opacity: 0.8;
    }

    /* 📋 Таблица */
    table {
        border-collapse: collapse;
        width: 100%;
        font-size: 1.2rem;
        animation: fadeIn 1s ease-in-out;
    }
    th, td {
        padding: 10px;
        text-align: center;
        border-bottom: 1px solid #444;
    }
    th {
        background-color: #222;
        color: gold;
    }
    tr:hover {
        background-color: #333;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)

# 🍁 Добавляем случайные листья
for i in range(10):
    st.markdown(
        f"<div class='leaf' style='left:{random.randint(0,90)}vw; animation-duration:{random.randint(8,15)}s; animation-delay:{random.random()*5}s;'>🍁</div>",
        unsafe_allow_html=True
    )

# ⚙️ Подключение к Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Аркуш1", ttl=5)
except Exception:
    st.error("❌ Помилка зчитування Google Sheets. Перевір посилання або доступ.")
    st.stop()

# 🧮 Если таблица пустая — создаем шаблон
if df is None or df.empty:
    df = pd.DataFrame(columns=["Місце", "Ім'я", "Клуб", "Вид", "Оцінка"])

# 👑 Добавляем корону лидеру
if not df.empty:
    try:
        df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")
        df = df.sort_values(by="Оцінка", ascending=False)
        df.iloc[0, df.columns.get_loc("Ім'я")] = "👑 " + str(df.iloc[0]["Ім'я"])
    except Exception:
        pass

# 📊 Отображаем таблицу
st.markdown(
    df.to_html(index=False, escape=False),
    unsafe_allow_html=True
)

# 🔁 Автообновление
st.markdown("<p style='text-align:center; color:gray;'>⏳ Оновлення кожні 5 секунд</p>", unsafe_allow_html=True)
time.sleep(5)
st.experimental_rerun()

# 🧾 Форма добавления данных (внизу страницы)
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("➕ Додати учасницю")

with st.form("add_participant", clear_on_submit=True):
    place = st.text_input("Місце")
    name = st.text_input("Ім'я")
    club = st.text_input("Клуб")
    apparatus = st.text_input("Вид")
    score = st.text_input("Оцінка")

    submitted = st.form_submit_button("Додати")

    if submitted:
        if name:
            new_row = pd.DataFrame([[place, name, club, apparatus, score]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            conn.update(worksheet="Аркуш1", data=df)
            st.success(f"✅ Учасницю {name} додано!")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.warning("⚠️ Введіть ім'я учасниці перед збереженням.")
