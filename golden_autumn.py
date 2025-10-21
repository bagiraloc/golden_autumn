import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# === ПОДКЛЮЧЕНИЕ К GOOGLE TABLE ===
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit?gid=0#gid=0"
SHEET_NAME = "Участницы"  # <-- замени, если лист называется иначе

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]

creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPE)
client = gspread.authorize(creds)
spreadsheet = client.open_by_url(SPREADSHEET_URL)

try:
    worksheet = spreadsheet.worksheet(SHEET_NAME)
except gspread.WorksheetNotFound:
    st.error(f"❌ Лист '{SHEET_NAME}' не найден! Проверь точное название вкладки в Google Sheets.")
    st.stop()

# === ФУНКЦИИ ===
def load_data():
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def add_participant(name, country, score):
    worksheet.append_row([name, country, score])
    st.success(f"✅ Участница {name} добавлена!")

# === НАСТРОЙКА СТРАНИЦЫ ===
st.set_page_config(page_title="Golden Autumn", page_icon="🍂", layout="wide")

# === CSS: оформление и анимация листьев ===
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #ffecd2, #fcb69f);
    font-family: 'Segoe UI', sans-serif;
    color: #3a2c1a;
}
h1, h2, h3 {
    text-align: center;
    color: #6b4226;
}
.leaf {
    position: fixed;
    top: -10%;
    animation: fall 10s linear infinite;
}
@keyframes fall {
    0% {transform: translateY(-10%) rotate(0deg);}
    100% {transform: translateY(110vh) rotate(720deg);}
}
</style>
""", unsafe_allow_html=True)

# === Титул ===
st.title("🍂 Турнир Golden Autumn")
st.markdown("<h3>Добавляйте участниц и следите за результатами онлайн!</h3>", unsafe_allow_html=True)

# === Боковое меню ===
menu = st.sidebar.radio("Меню", ["🏃‍♀️ Добавить участницу", "🏆 Таблица турнира"])

# === Добавление участниц ===
if menu == "🏃‍♀️ Добавить участницу":
    with st.form("add_form"):
        name = st.text_input("Имя участницы")
        country = st.text_input("Страна")
        score = st.text_input("Оценка")

        submitted = st.form_submit_button("Добавить")

        if submitted:
            if not name or not score:
                st.warning("⚠️ Введите имя и оценку.")
            else:
                try:
                    add_participant(name, country, score)
                except Exception as e:
                    st.error(f"Ошибка при добавлении: {e}")

# === Таблица турнира ===
elif menu == "🏆 Таблица турнира":
    df = load_data()

    if df.empty:
        st.info("Пока нет данных. Добавь участниц!")
    else:
        # Приводим оценки к числам
        if "Оцінка" in df.columns:
            df["Оцінка"] = df["Оцінка"].apply(lambda x: float(str(x).replace(",", ".")) if str(x).replace(",", ".").replace('.', '', 1).isdigit() else 0)
            df = df.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
            df.index += 1
        else:
            st.warning("⚠️ В таблице нет колонки 'Оцінка'. Проверь Google Sheet.")
        
        st.subheader("🏆 Рейтинг участниц")
        st.dataframe(df, use_container_width=True)

        # Топ 3
        if not df.empty:
            top3 = df.head(3)
            st.markdown("### 🥇 Топ 3 участницы")
            for i, row in top3.iterrows():
                st.markdown(f"**{i}. {row.get('Имя', '—')} ({row.get('Страна', '—')}) — {row.get('Оцінка', 0)} баллов**")
