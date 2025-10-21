import streamlit as st
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.animate import animate

# 🏆 Заголовок
st.set_page_config(page_title="Золота Осінь 2025", page_icon="👑", layout="wide")
st.markdown("<h1 style='text-align: center;'>👑 Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)

# 🔗 ПРЯМОЕ подключение к твоей таблице
sheet_url = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit?gid=0"
conn = st.connection("gsheets", type=GSheetsConnection, url=sheet_url)

# 🕒 Автоматичне оновлення кожні 5 секунд
st_autorefresh = st.experimental_rerun

def load_data():
    try:
        df = conn.read(worksheet="Аркуш1", ttl=5)
        df = df.dropna(subset=["Ім'я"])  # прибираємо порожні рядки
        return df
    except Exception as e:
        st.error(f"❌ Помилка зчитування Google Sheets: {e}")
        return pd.DataFrame(columns=["Ім'я", "Бали"])

def save_data(df):
    try:
        conn.update(worksheet="Аркуш1", data=df)
    except Exception as e:
        st.error(f"❌ Помилка збереження: {e}")

# 📥 Завантаження даних
df = load_data()

# 🧾 Відображення таблиці з анімацією
st.markdown("### 🏅 Турнірна таблиця")
if not df.empty:
    with stylable_container("animated_table", key="table_anim"):
        for i, row in df.iterrows():
            animate(f"<b>{row['Ім\'я']}</b> — <b>{row['Бали']} 🏆</b>")
else:
    st.info("Немає учасниць поки що 😌")

# 📋 Форма додавання нової учасниці (внизу сторінки)
st.markdown("---")
st.markdown("### ➕ Додати учасницю")

with st.form("add_participant", clear_on_submit=True):
    name = st.text_input("Ім'я учасниці")
    score = st.number_input("Бали", min_value=0, max_value=1000, value=0, step=1)
    submitted = st.form_submit_button("💾 Зберегти")

if submitted:
    if name:
        new_row = pd.DataFrame({"Ім'я": [name], "Бали": [score]})
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success("✅ Додано!")
        time.sleep(1)
        st.rerun()
    else:
        st.warning("⚠️ Введіть ім'я!")

# 🔁 Автооновлення кожні 5 секунд
time.sleep(5)
st.rerun()
