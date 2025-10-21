import streamlit as st
import pandas as pd
import json, time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit.components.v1 import html

# ---------- НАСТРОЙКИ ----------
st.set_page_config(page_title="👑 Золота Осінь 2025 🍁", layout="wide")

# ---------- ПОДКЛЮЧЕНИЕ К GOOGLE SHEETS ----------
sa_json = json.loads(st.secrets["gsheets_service_account"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(sa_json, scope)
client = gspread.authorize(creds)

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit#gid=0"
sheet = client.open_by_url(SPREADSHEET_URL).sheet1

# ---------- ЗАГРУЗКА И СОХРАНЕНИЕ ----------
def load_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_data(df):
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# ---------- UI ----------
st.markdown(
    "<h1 style='text-align:center;'>👑 Золота Осінь 2025 🍁</h1>",
    unsafe_allow_html=True
)

# ---------- ТАБЛИЦА ----------
placeholder = st.empty()

# функция плавного обновления
def render_table():
    df = load_data()
    if df.empty:
        st.warning("Поки що немає учасниць 👩‍🌾")
    else:
        # Сортировка по сумме баллов (если есть колонка 'Бали')
        if 'Бали' in df.columns:
            df = df.sort_values(by='Бали', ascending=False)

        # Автоматическое уменьшение таблицы при большом количестве строк
        max_height = min(600, 100 + len(df) * 40)
        html_table = df.to_html(index=False, justify='center', border=0)
        html(
            f"""
            <div style='text-align:center; font-size:22px;'>
                <img src="https://cdn-icons-png.flaticon.com/512/616/616408.png" width="50">
                <div style='height:{max_height}px; overflow:auto;'>
                    {html_table}
                </div>
            </div>
            <script>
                const table = document.querySelector('table');
                table.style.animation = 'fadein 1s ease';
                const style = document.createElement('style');
                style.innerHTML = `
                    @keyframes fadein {{ from {{opacity:0; transform:translateY(10px)}} to {{opacity:1; transform:translateY(0)}} }}
                    table {{ animation: fadein 1s; width:80%; margin:auto; border-collapse:collapse; }}
                    th, td {{ padding:10px; border-bottom:1px solid #ddd; }}
                    th {{ background:#f9f3d2; }}
                `;
                document.head.appendChild(style);
            </script>
            """,
            height=max_height + 120,
        )

# ---------- ОСНОВНОЙ ЦИКЛ ОБНОВЛЕНИЯ ----------
render_table()
st_autorefresh = st.empty()

# ---------- ФОРМА ВВОДА ----------
st.markdown("---")
st.subheader("➕ Додати учасницю")

with st.form("add_form", clear_on_submit=True):
    name = st.text_input("Ім’я")
    score = st.number_input("Бали", min_value=0, step=1)
    submit = st.form_submit_button("💾 Зберегти")

if submit and name:
    df = load_data()
    df = pd.concat([df, pd.DataFrame({"Ім’я": [name], "Бали": [score]})], ignore_index=True)
    save_data(df)
    st.success(f"✅ {name} додано!")
    time.sleep(1)
    st.experimental_rerun()

# Автообновление каждые 5 секунд
st_autorefresh.write("<meta http-equiv='refresh' content='5'>", unsafe_allow_html=True)
