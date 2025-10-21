import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ===============================
# Підключення до Google таблиці
# ===============================

SHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit"

# JSON-файл ключа, який ти додала в Codespaces або поруч із проєктом
SERVICE_ACCOUNT_FILE = "service_account.json"

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(SHEET_URL).sheet1

# ====================================
# Ініціалізація Streamlit стану (пам’ять)
# ====================================

if "results" not in st.session_state:
    data = sheet.get_all_records()
    st.session_state.results = pd.DataFrame(data)

# ===============================
# Заголовок і форма
# ===============================

st.title("🏆 Турнір «Golden Autumn»")

with st.form("add_form"):
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        name = st.text_input("Ім'я учасниці")
    with c2:
        club = st.text_input("Клуб")
    with c3:
        category = st.text_input("Категорія")
    with c4:
        score = st.text_input("Оцінка (наприклад 27.75)")
    with c5:
        add_btn = st.form_submit_button("➕ Додати")

# ===============================
# Додавання учасниці в таблицю
# ===============================

if add_btn:
    if not name.strip():
        st.error("Введіть ім'я учасниці!")
    else:
        try:
            score_val = None

            # якщо введено оцінку — пробуємо перетворити у число
            if score and score.strip():
                score_val = float(score.replace(",", "."))

            # формуємо новий рядок
            new_row = {
                "Місце": None,
                "Ім'я": name.strip(),
                "Клуб": club.strip(),
                "Оцінка": score_val,
                "Категорія": category.strip()
            }

            # додаємо до DataFrame
            df = st.session_state.results.copy()
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            # сортуємо за оцінкою (NaN внизу)
            df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")
            df = df.sort_values(by="Оцінка", ascending=False, na_position="last")

            st.session_state.results = df
            st.session_state.last_added = name.strip()

            # додаємо у Google Sheets
            sheet.append_row([
                name.strip(),
                club.strip(),
                score_val if score_val is not None else "",
                category.strip()
            ])

            st.success(f"✅ Учасницю {name} додано до таблиці!")

            # оновлюємо сторінку
            st.experimental_rerun()

        except Exception as e:
            st.error(f"❌ Помилка при додаванні: {e}")

# ===============================
# Відображення таблиці
# ===============================

st.subheader("📋 Поточні результати")
st.dataframe(st.session_state.results)
