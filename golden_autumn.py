import streamlit as st
import pandas as pd
import random
import gspread
import json
from google.oauth2.service_account import Credentials
from urllib.parse import urlparse, parse_qs

# ---------------- Настройки страницы ----------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# ---------------- Настройки подключения к Google Sheets ----------------
# Внимание: в Secrets должен быть сервисный JSON под ключом 'gcp_service_account'
# Пример: st.secrets["gcp_service_account"] -> dict или JSON-строка
SHEET_URL = st.secrets.get("sheet_url", "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit")
# Название листа (если переименовали) можно положить в secrets['sheet_name'] или изменить здесь:
SHEET_NAME = st.secrets.get("sheet_name", "Аркуш1")  # <- поменяйте на текущее имя листа

# Функция: вернуть spreadsheet id из URL
def sheet_id_from_url(url):
    try:
        parts = url.split("/")
        # обычно id находится между /d/ and /edit
        if "/d/" in url:
            return parts[parts.index("d") + 1] if "d" in parts else url.split("/d/")[1].split("/")[0]
        # fallback: parse query
        q = parse_qs(urlparse(url).query)
        return q.get("id", [None])[0]
    except Exception:
        return None

# Попытка загрузки service account из secrets
def get_credentials_from_secrets():
    if "gcp_service_account" not in st.secrets:
        raise RuntimeError("В st.secrets не найден ключ 'gcp_service_account'. Добавьте JSON сервисного аккаунта.")
    sa = st.secrets["gcp_service_account"]
    # sa может быть dict (если вы вставляли объект), либо строкой JSON
    if isinstance(sa, str):
        sa = json.loads(sa)
    # Scope
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(sa, scopes=scopes)
    return creds

# Открыть таблицу и вернуть Worksheet (gspread)
def open_worksheet():
    creds = get_credentials_from_secrets()
    gc = gspread.authorize(creds)
    sid = sheet_id_from_url(SHEET_URL)
    if not sid:
        raise RuntimeError("Не удалось разобрать ID таблицы по URL. Проверьте sheet_url в secrets.")
    sh = gc.open_by_key(sid)
    try:
        ws = sh.worksheet(SHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        # если лист не найден — попробуем по индексу 0
        ws = sh.get_worksheet(0)
    return ws

# ---------- Стили и анимация CSS ----------
def render_css(font_px):
    css = f"""
    <style>
    body {{ background-color: #0d0d0d; color: #f6c453; overflow-x: hidden; }}
    h1 {{ text-align: center; color: #f6c453; font-weight: bold; text-shadow: 0 0 20px #f6c453;
         animation: glow 2s ease-in-out infinite alternate; }}
    @keyframes glow {{ from {{ text-shadow: 0 0 10px #f6c453; }} to {{ text-shadow: 0 0 35px #ffd700; }} }}
    .leaf {{ position: fixed; top: -10vh; color: #ffd700; font-size: 28px; opacity: 0.8; animation: fall linear infinite; z-index: -1; }}
    @keyframes fall {{ 0% {{ transform: translateY(0) rotate(0deg); }} 100% {{ transform: translateY(110vh) rotate(360deg); }} }}
    table {{ width: 100%; border-collapse: collapse; background: rgba(30,30,30,0.9); border-radius: 14px; box-shadow: 0 0 20px rgba(246,196,83,0.3); font-size: {font_px}; }}
    th, td {{ padding: 6px; text-align: center; color: #f6c453; word-break: break-word; }}
    th {{ background-color: #1e1e1e; border-bottom: 2px solid #f6c453; }}
    tr.highlight {{ animation: slideUp 0.8s ease-out; }}
    @keyframes slideUp {{ from {{ transform: translateY(50px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
    .crown {{ animation: crownPulse 3s ease-in-out infinite; }}
    @keyframes crownPulse {{ 0%,100% {{ text-shadow: 0 0 10px #ffd700; }} 50% {{ text-shadow: 0 0 25px #ffea00; }} }}
    .stButton>button {{ background: linear-gradient(90deg, #f6c453, #b8860b); color: #0d0d0d !important; border: none; border-radius: 8px; font-weight: bold; padding: 0.6rem 1.2rem; }}
    .stButton>button:hover {{ background: linear-gradient(90deg, #ffd700, #f6c453); }}
    </style>
    """
    return css

# ---------- Листочки (HTML) ----------
def render_leaves(n=20):
    leaves_html = ""
    for i in range(n):
        left = random.randint(0, 100)
        duration = round(random.uniform(12, 28), 2)
        delay = round(random.uniform(0, 20), 2)
        leaf = random.choice(["🍁","🍁","🍂","🍁"])
        leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s;">{leaf}</div>'
    return leaves_html

# ---------------- Основная логика ----------------
# 1) Читаем с листа в DataFrame (если есть) — иначе пустой DF
def read_sheet_df():
    try:
        ws = open_worksheet()
        data = ws.get_all_values()  # список списков
        if not data or len(data) <= 1:
            # если только заголовки нет данных -> пустой df
            if data:
                cols = data[0]
            else:
                cols = ["Місце","Ім’я","Клуб","Вид","Оцінка"]
            return pd.DataFrame(columns=cols)
        df = pd.DataFrame(data[1:], columns=data[0])
        # Поправка типов для "Оцінка" если есть
        if "Оцінка" in df.columns:
            def to_float_safe(x):
                try:
                    return float(str(x).replace(",","."))
                except:
                    return None
            df["Оцінка"] = df["Оцінка"].apply(to_float_safe)
        return df
    except Exception as e:
        st.error(f"Помилка підключення до Google Sheets: {e}")
        return pd.DataFrame(columns=["Місце","Ім’я","Клуб","Вид","Оцінка"])

# Записать весь DF обратно в лист (перезапись)
def write_sheet_df(df):
    try:
        ws = open_worksheet()
        # Преобразуем Оцінка к строке с 3 знаками и запятой
        df_to_write = df.copy()
        if "Оцінка" in df_to_write.columns:
            df_to_write["Оцінка"] = df_to_write["Оцінка"].map(lambda x: f"{x:.3f}" if pd.notna(x) else "")
        values = [df_to_write.columns.tolist()] + df_to_write.astype(str).values.tolist()
        ws.clear()
        ws.update(values)
        return True
    except Exception as e:
        st.error(f"Помилка запису в Google Sheets: {e}")
        return False

# ---------- UI ----------
# Загружаем данные (с листа)
df_sheet = read_sheet_df()

# Если колонки неправильные — приводим к нужным
expected_cols = ["Місце","Ім’я","Клуб","Вид","Оцінка"]
for col in expected_cols:
    if col not in df_sheet.columns:
        df_sheet[col] = None
df_sheet = df_sheet[expected_cols]

# Сохраним в session_state копию
if "results" not in st.session_state:
    # если в Google Sheets есть данные — взять их, преобразовать
    st.session_state.results = df_sheet.copy()
    # Если "Оцінка" — преобразовать к float
    if "Оцінка" in st.session_state.results.columns:
        st.session_state.results["Оцінка"] = st.session_state.results["Оцінка"].apply(lambda x: float(str(x).repl
