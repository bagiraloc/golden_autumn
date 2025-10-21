import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Золота Осінь 2025 🍂", layout="centered")

st.title("Золота Осінь 2025 🍂")

try:
    # 🔹 Підключення до Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)

    # 🔹 Зчитування таблиці (вкажи свій Spreadsheet ID!)
    # ID — це частина посилання між /d/ і /edit
    sheet_id = "1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY"
    df = conn.read(spreadsheet=sheet_id, worksheet="Лист1")

    # Якщо таблиця порожня — створимо початкову структуру
    if df.empty:
        df = pd.DataFrame(columns=["Ім'я", "Оцінка"])

    # 🔹 Форма для додавання учасниць
    st.subheader("➕ Додати учасницю")

    with st.form("add_participant"):
        name = st.text_input("Ім'я учасниці")
        score = st.number_input("Оцінка", 0, 100)
        submitted = st.form_submit_button("Додати")

        if submitted:
            if name.strip() == "":
                st.error("Введи ім'я!")
            else:
                new_row = pd.DataFrame([[name, score]], columns=["Ім'я", "Оцінка"])
                df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Лист1", data=df)
                st.success(f"✅ {name} додано!")

    # 🔹 Відображення списку учасниць
    st.subheader("📋 Учасниці")
    st.dataframe(df)

except Exception as e:
    st.error("❌ Помилка при з'єднанні з Google Sheets")
    st.exception(e)
