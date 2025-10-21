# golden_autumn.py
import streamlit as st
import pandas as pd
import random
import json
import math

# Google sheets
try:
    import gspread
    from google.oauth2.service_account import Credentials
except Exception:
    gspread = None
    Credentials = None

# ---------------- Настройка страницы ----------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# ---------------- CSS ----------------
# font-size в таблице будет вычисляться динамически ниже
base_css = """
<style>
body {
    background-color: #0d0d0d;
    color: #f6c453;
    overflow-x: hidden;
}
h1 {
    text-align: center;
    color: #f6c453;
    font-weight: bold;
    text-shadow: 0 0 20px #f6c453;
    animation: glow 2s ease-in-out infinite alternate;
    margin-top: 10px;
}
@keyframes glow {
    from { text-shadow: 0 0 10px #f6c453; }
    to { text-shadow: 0 0 35px #ffd700; }
}
.leaf {
    position: fixed;
    top: -10vh;
    color: #ffd700;
    font-size: 28px;
    opacity: 0.8;
    animation: fall linear infinite;
    z-index: 1;
    pointer-events: none;
}
@keyframes fall {
    0% { transform: translateY(0) rotate(0deg); }
    100% { transform: translateY(110vh) rotate(360deg); }
}
.table-wrap {
    width: 96%;
    margin: 18px auto 30px auto;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 30px rgba(246,196,83,0.08);
}
table {
    width: 100%;
    border-collapse: collapse;
    background: rgba(30,30,30,0.95);
}
th, td {
    padding: 6px 10px;
    text-align: center;
    color: #f6c453;
    border-bottom: 1px solid rgba(246,196,83,0.06);
    word-break: break-word;
}
th {
    background-color: rgba(22,22,22,0.95);
    border-bottom: 2px solid #f6c453;
    font-weight: 700;
}
tr.highlight {
    animation: slideUp 0.6s ease-out;
    background: linear-gradient(90deg, rgba(246,196,83,0.06), rgba(246,196,83,0.02));
}
@keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
.crown {
    animation: crownPulse 3s ease-in-out infinite;
}
@keyframes crownPulse {
    0%, 100% { text-shadow: 0 0 10px #ffd700; }
    50% { text-shadow: 0 0 22px #ffea00; }
}
.stButton>button {
    background: linear-gradient(90deg, #f6c453, #b8860b);
    color: #0d0d0d !important;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    padding: 0.6rem 1.2rem;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #ffd700, #f6c453);
}
</style>
"""

st.markdown(base_css, unsafe_allow_html=True)

# ---------------- Листочки ----------------
leaves_html = ""
for i in range(20):
    left = random.randint(0, 100)
    duration = random.uniform(12, 26)
    delay = random.uniform(0, 20)
    size = random.randint(20, 36)
    leaf = random.choice(["🍁", "🍂"])
    leaves_html += (
        f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; '
        f'animation-delay:{delay}s; font-size:{size}px;">{leaf}</div>'
    )
st.markdown(leaves_html, unsafe_allow_html=True)

st.markdown("<h1>👑 Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)

# ---------------- Google Sheets: подключение ----------------
# берем URL/ID и имя листа из secrets (если есть), иначе можно задать вручную
SHEET_URL = st.secrets.get("SHEET_URL", None) if st.secrets else None
SHEET_NAME = st.secrets.get("SHEET_NAME", "Лист1") if st.secrets else "Лист1"

def get_gspread_client():
    """Попытка получить gspread клиент из секрета или файла."""
    if gspread is None or Credentials is None:
        return None, "gspread или google-auth не установлены"

    # 1) сначала пробуем st.secrets["SERVICE_ACCOUNT_JSON"]
    service_json = None
    if st.secrets and "SERVICE_ACCOUNT_JSON" in st.secrets:
        service_json = st.secrets["SERVICE_ACCOUNT_JSON"]
    else:
        # 2) пробуем локальный файл service_account.json
        try:
            with open("service_account.json", "r", encoding="utf-8") as f:
                service_json = f.read()
        except Exception:
            service_json = None

    if not service_json:
        return None, "Не найден JSON ключа (st.secrets['SERVICE_ACCOUNT_JSON'] или файл service_account.json)"

    try:
        info = json.loads(service_json)
        creds = Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
        client = gspread.authorize(creds)
        return client, None
    except Exception as e:
        return None, f"Ошибка авторизации Google: {e}"

# ---------------- Состояние таблицы в session_state ----------------
if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
if "last_added" not in st.session_state:
    st.session_state.last_added = None
if "added_ids" not in st.session_state:
    st.session_state.added_ids = set()  # чтобы не дублировать при повторном нажатии

# Если указан Google Sheet URL, пробуем загрузить существующие данные
gsheet_client, gsheet_error = get_gspread_client()
if SHEET_URL and gsheet_client:
    try:
        # откроем таблицу
        ss = gsheet_client.open_by_url(SHEET_URL)
        try:
            ws = ss.worksheet(SHEET_NAME)
        except Exception:
            # попробуем по индексу 0
            ws = ss.get_worksheet(0)
        rows = ws.get_all_records()
        if rows:
            df = pd.DataFrame(rows)
            # нормализуем столбцы: ищем похожие названия
            expected_cols = ["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"]
            # если у пользователя английские/другие названия — попытаемся подобрать:
            col_map = {}
            for c in df.columns:
                cl = c.strip().lower()
                if "name" in cl or "ім" in cl:
                    col_map[c] = "Ім’я"
                elif "club" in cl or "клуб" in cl:
                    col_map[c] = "Клуб"
                elif "place" in cl or "міс" in cl:
                    col_map[c] = "Місце"
                elif "score" in cl or "оцін" in cl:
                    col_map[c] = "Оцінка"
                elif "вид" in cl or "category" in cl:
                    col
