import streamlit as st
import pandas as pd
import random
import time
from streamlit_gsheets import GSheetsConnection

# ------------------ Настройка страницы ------------------
st.set_page_config(page_title="Золота Осінь 2025", page_icon="🍁", layout="wide")

# ------------------ Параметры Google Sheet ------------------
# вот ссылка, которую ты давала
SHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY/edit?gid=0"

# ------------------ Стили и анимации (тёмная тема) ------------------
st.markdown(
    """
    <style>
    :root{
      --gold:#f6c453;
      --gold-strong:#ffd700;
      --bg:#0b0d10;
      --panel:#121416;
      --muted:#cfcfcf;
    }
    html, body, .stApp {
      background: linear-gradient(180deg, var(--bg), #0f1113) !important;
      color: var(--muted) !important;
    }
    .title {
      text-align:center;
      font-size:34px;
      color:var(--gold);
      font-weight:700;
      text-shadow: 0 0 18px rgba(246,196,83,0.18);
      margin: 8px 0 18px 0;
    }
    /* leaves (only maple 🍁) */
    .leaf {
      position: fixed;
      top: -8vh;
      font-size: 28px;
      color: var(--gold-strong);
      opacity: 0.95;
      animation-name: fall;
      animation-timing-function: linear;
      animation-iteration-count: infinite;
      z-index: 0;
      pointer-events: none;
    }
    @keyframes fall {
      0% { transform: translateY(-5vh) rotate(0deg); opacity: 1; }
      100% { transform: translateY(120vh) rotate(360deg); opacity: 0.25; }
    }

    /* table look */
    .results-wrap { width:100%; overflow:auto; }
    table.results {
      width:100%;
      border-collapse: collapse;
      background: rgba(18,20,22,0.85);
      color: var(--muted);
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
      overflow: hidden;
      font-size:16px;
    }
    table.results th, table.results td {
      padding: 10px 12px;
      text-align: center;
      border-bottom: 1px solid rgba(246,196,83,0.04);
    }
    table.results th {
      background: rgba(20,22,24,0.9);
      color: var(--gold);
      font-weight:600;
    }

    /* first place crown pulsing */
    .crown {
      display:inline-block;
      animation: crownPulse 3s ease-in-out infinite;
      color: var(--gold-strong);
      text-shadow: 0 0 8px rgba(255,215,0,0.6);
    }
    @keyframes crownPulse {
      0% { transform: scale(1); filter: drop-shadow(0 0 6px rgba(255,215,0,0.2)); }
      50% { transform: scale(1.08); filter: drop-shadow(0 0 20px rgba(255,215,0,0.6)); }
      100% { transform: scale(1); filter: drop-shadow(0 0 6px rgba(255,215,0,0.2)); }
    }

    /* animation when new participant appears - slide from bottom into place */
    tr.new-row {
      animation: slideUpFromBottom 0.9s cubic-bezier(.2,.9,.3,1) both;
      background: linear-gradient(90deg, rgba(255,215,0,0.06), rgba(255,215,0,0.01));
    }
    @keyframes slideUpFromBottom {
      0% { transform: translateY(60px); opacity: 0; }
      100% { transform: translateY(0); opacity: 1; }
    }

    /* subtle highlight for every row on hover */
    table.results tbody tr:hover { background: rgba(246,196,83,0.03); }

    /* buttons */
    .stButton>button {
      background: linear-gradient(90deg, var(--gold), #b8860b);
      color: #0b0d10 !important;
      border-radius: 8px;
      padding: 8px 14px;
      font-weight:600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ Функция отображения кленовых листьев ------------------
def render_maple_leaves(count: int = 18):
    html = ""
    for i in range(count):
        left = random.randint(0, 95)
        duration = round(random.uniform(7.5, 14.0), 2)
        delay = round(random.uniform(0, 8.0), 2)
        size = random.randint(22, 40)
        html += (
            f'<div class="leaf" style="left:{left}%; animation-duration:{duration}s; animation-delay:{delay}s; font-size:{size}px;">🍁</div>'
        )
    st.markdown(html, unsafe_allow_html=True)

# render leaves once (they will animate via CSS)
render_maple_leaves(18)

st.markdown('<div class="title">Золота Осінь 2025</div>', unsafe_allow_html=True)

# ------------------ Подключение к Google Sheets ------------------
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("❌ Невдале з'єднання зі службою Google Sheets (помилка підключення).")
    st.exception(e)
    st.stop()

# ------------------ Загрузка данных из таблицы ------------------
def load_sheet():
    try:
        # читаем всю таблицу; библиотека может вернуть DataFrame или список словарей
        df = conn.read(spreadsheet=SHEET_URL)
        if isinstance(df, pd.DataFrame):
            return df.copy()
        else:
            return pd.DataFrame(df)
    except Exception as e:
        # если не удалось — вернём пустой DF с нужными колонками
        return pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])

df = load_sheet()

# если таблица пустая — создать каркас с нужными колонками (чтобы UI не ломался)
expected_cols = ["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"]
for c in expected_cols:
    if c not in df.columns:
        df[c] = pd.NA
df = df[expected_cols]

# ------------------ Инициализация session_state ------------------
if "last_added_key" not in st.session_state:
    st.session_state.last_added_key = None  # ключ для идентификации последней добавленной строки

# helper to make a unique key for a participant (name+score+timestamp)
def make_part_key(name: str, score: float):
    return f"{name}__{score}__{int(time.time()*1000)}"

# ------------------ Форма добавления участницы ------------------
with st.expander("🔒 Панель судді", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    name = c1.text_input("Ім’я (ПІБ)")
    club = c2.text_input("Клуб")
    event = c3.text_input("Вид")
    score_text = c4.text_input("Оцінка (напр. 27.800)")

    col_add, col_clear = st.columns([1,1])
    add_btn = col_add.button("➕ Додати учасницю")
    clear_btn = col_clear.button("🧹 Очистити таблицю")

# ------------------ Логика добавления ------------------
if add_btn:
    if not (name and score_text):
        st.warning("Введіть, будь ласка, ім'я та оцінку.")
    else:
        try:
            score_val = float(score_text.replace(",", "."))
        except ValueError:
            st.error("Неправильний формат оцінки — використайте цифри, наприклад 27.800")
        else:
            # считываем свежие данные (на момент добавления)
            df_current = load_sheet()
            # убедимся, что есть нужные колонки
            for c in expected_cols:
                if c not in df_current.columns:
                    df_current[c] = pd.NA
            df_current = df_current[expected_cols]

            # создаём новую строку
            new_row = pd.DataFrame([[None, name, club, event, score_val]], columns=expected_cols)

            # объединяем
            updated = pd.concat([df_current, new_row], ignore_index=True)
