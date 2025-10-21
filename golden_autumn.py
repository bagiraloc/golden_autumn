import streamlit as st
import pandas as pd
import gspread
import json
import time
from oauth2client.service_account import ServiceAccountCredentials
from google.auth.exceptions import DefaultCredentialsError
from streamlit_extras.stylable_container import stylable_container

# --- Налаштування сторінки ---
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# --- Заголовок ---
st.markdown(
    "<h1 style='text-align: center; color: #d4af37;'>👑 Золота Осінь 2025 🍂</h1>",
    unsafe_allow_html=True,
)

# --- Підключення до Google Sheets ---
try:
    sa_json = json.loads(st.secrets["gsheets_service_account"])
except Exception as e:
    st.error("❌ Не знайдено або невірно вказано 'gsheets_service_account' у Streamlit Secrets.")
    st.stop()

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(sa_json, SCOPE)
gc = gspread.authorize(creds)

# --- ID таблиці (твоя таблиця) ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit?gid=0"
SHEET_ID = SHEET_URL.split("/d/")[1].split("/")[0]
sheet = gc.open_by_key(SHEET_ID).sheet1

# --- Функція для зчитування даних ---
def load_data():
    data = sheet.get_all_records()
    if not data:
        return pd.DataFrame(columns=["Місце", "Ім'я", "Клуб", "Вид", "Оцінка"])
    df = pd.DataFrame(data)
    df = df.sort_values(by=["Місце"], ascending=True)
    return df

# --- Функція для запису нових даних ---
def save_data(df):
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# --- Завантаження даних ---
df = load_data()

# --- Таблиця з анімацією ---
st.markdown("---")
st.markdown("### 🏆 Поточні результати:")

if not df.empty:
    st.dataframe(
        df.style.set_properties(
            **{
                "text-align": "center",
                "border": "1px solid #d4af37",
                "background-color": "#1E1E1E",
                "color": "#FFD700",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Поки що немає учасниць 😌")

# --- Форма додавання ---
st.markdown("---")
st.markdown("### ➕ Додати нову учасницю:")

with stylable_container(
    key="add_form",
    css_styles="""
        border: 2px solid #FFD700;
        padding: 1rem;
        border-radius: 1rem;
        background-color: #222;
    """,
):
    with st.form("add_competitor"):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            place = st.number_input("Місце", min_value=1, step=1)
        with col2:
            name = st.text_input("Ім'я")
        with col3:
            club = st.text_input("Клуб")
        with col4:
            apparatus = st.text_input("Вид")
        with col5:
            score = st.number_input("Оцінка", min_value=0.0, step=0.01)

        submitted = st.form_submit_button("💾 Зберегти")

        if submitted:
            if name.strip() == "":
                st.warning("Введіть ім’я учасниці!")
            else:
                new_row = pd.DataFrame(
                    [[int(place), name, club, apparatus, float(score)]],
                    columns=["Місце", "Ім'я", "Клуб", "Вид", "Оцінка"],
                )
                df = pd.concat([df, new_row], ignore_index=True)
                df = df.sort_values(by=["Місце"])
                save_data(df)
                st.success(f"✅ Учасницю **{name}** додано!")
                st.experimental_rerun()

# --- Автоматичне оновлення ---
st.markdown(
    """
    <script>
    setTimeout(function(){
        window.location.reload(1);
    }, 10000);
    </script>
    """,
    unsafe_allow_html=True,
)
