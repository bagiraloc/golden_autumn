import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("🏅 Таблиця учасниць")

# Підключення
conn = st.connection("gsheets", type=GSheetsConnection)

# ID Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit?gid=0"

# Завантаження даних
try:
    df = conn.read(spreadsheet=SHEET_URL)
except Exception as e:
    st.error(f"Помилка при з'єднанні з Google Sheets: {e}")
    st.stop()

# Форма для додавання
with st.form("add_participant"):
    name = st.text_input("Ім'я учасниці")
    score = st.number_input("Оцінка", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Додати")

    if submitted and name:
        new_row = pd.DataFrame({"Ім'я": [name], "Оцінка": [score]})
        df = pd.concat([df, new_row], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, data=df)
        st.success(f"✅ Додано: {name} — {score}")

# Показ таблиці
st.dataframe(df)
