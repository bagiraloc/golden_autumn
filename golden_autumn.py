import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import random

# --- GOOGLE SHEETS НАСТРОЙКА ---
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit?gid=0"

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("streamlit-gsheets.json", SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open_by_url(SPREADSHEET_URL).sheet1

# --- ФУНКЦИИ ---
def load_data():
    data = SHEET.get_all_records()
    return pd.DataFrame(data)

def add_participant(misce, name, club, vid, ocinka):
    SHEET.append_row([misce, name, club, vid, ocinka])

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="Золота Осінь 2025", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    body { background-color: #0E1117; color: white; font-family: "Arial"; }
    .title { text-align: center; font-size: 40px; font-weight: bold; color: #FFD700; }
    .autumn { text-align: center; font-size: 30px; color: #FF7F50; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { border: 1px solid #FFD700; padding: 10px; text-align: center; }
    th { background-color: #2B2B2B; color: #FFD700; }
    tr:nth-child(even) { background-color: #1E1E1E; }
    tr:hover { background-color: #333333; }
    </style>
""", unsafe_allow_html=True)

# --- ЗАГОЛОВОК ---
st.markdown('<div class="title">👑 Золота Осінь 2025 🍁</div>', unsafe_allow_html=True)

# --- АНІМАЦІЯ ЛИСТОЧКІВ ---
leaves = ["🍂", "🍁", "🍃"]
animated_leaves = "".join(random.choices(leaves, k=20))
st.markdown(f'<div class="autumn">{animated_leaves}</div>', unsafe_allow_html=True)

# --- ОТОБРАЖЕНИЕ ТАБЛИЦЫ ---
placeholder = st.empty()

def show_table():
    df = load_data()
    if df.empty:
        st.warning("Поки що немає учасниць 🌸")
    else:
        df = df.sort_values(by=["Місце"]).reset_index(drop=True)
        st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)

while True:
    with placeholder.container():
        show_table()
    time.sleep(5)
    placeholder.empty()

# --- ФОРМА ДЛЯ ДОДАВАННЯ ---
st.markdown("---")
st.subheader("➕ Додати учасницю:")

with st.form("add_form", clear_on_submit=True):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        misce = st.text_input("Місце")
    with col2:
        name = st.text_input("Ім’я")
    with col3:
        club = st.text_input("Клуб")
    with col4:
        vid = st.text_input("Вид")
    with col5:
        ocinka = st.text_input("Оцінка")

    submitted = st.form_submit_button("💫 Додати")

    if submitted and misce and name and club and vid and ocinka:
        add_participant(misce, name, club, vid, ocinka)
        st.success(f"✅ Учасницю {name} додано!")
        st.balloons()
