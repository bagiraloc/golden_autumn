# golden_autumn.py
import streamlit as st
import pandas as pd
import random
import os
import time
from datetime import datetime
import io

# -------------------- Налаштування сторінки --------------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# -------------------- Авто-перезавантаження через JS (5s) --------------------
# Це оновлює сторінку кожні 5 секунд, щоб підвантажувати зміни в results.csv
st.markdown(
    """
    <script>
    // перезавантаження сторінки кожні 5 секунд
    setTimeout(()=>{ window.location.reload(); }, 5000);
    </script>
    """,
    unsafe_allow_html=True,
)

# -------------------- CSS стиль та анімації --------------------
st.markdown(
    """
    <style>
    :root {
      --bg: #0b0b0b;
      --panel: #121212;
      --gold: #f6c453;
      --accent: #b8860b;
      --muted: #ddd6c9;
    }
    body, .stApp {
      background: linear-gradient(180deg, #050505 0%, #131313 100%);
      color: var(--gold);
    }
    h1.app-title {
      text-align: center;
      color: var(--gold);
      font-weight: 800;
      text-shadow: 0 0 25px rgba(246,196,83,0.2);
      font-size: 44px;
      margin-bottom: 0.5rem;
    }
    .subtitle {
      text-align:center;
      color: var(--muted);
      margin-bottom: 1.2rem;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      background: rgba(20,20,20,0.8);
      color: var(--gold);
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 6px 30px rgba(0,0,0,0.6);
    }
    th, td {
      padding: 12px 14px;
      text-align: center;
      font-size: 18px;
    }
    th {
      background: #1f1f1f;
      color: var(--gold);
      border-bottom: 2px solid rgba(246,196,83,0.12);
    }
    tr:nth-child(even) td { background: rgba(255,255,255,0.01); }
    .crown { font-weight: 800; text-shadow: 0 0 10px rgba(255,225,120,0.6); }
    .leaf {
      position: fixed;
      top: -10vh;
      color: var(--gold);
      opacity: 0.95;
      animation: fall linear infinite;
      z-index: 0;
      pointer-events: none;
    }
    @keyframes fall {
      0% { transform: translateY(-10vh) rotate(0deg); }
      100% { transform: translateY(110vh) rotate(360deg); }
    }
    .new-row {
      animation: slideUp 0.8s ease-out;
      background: linear-gradient(90deg, rgba(246,196,83,0.06), rgba(246,196,83,0.02));
    }
    @keyframes slideUp {
      from { transform: translateY(30px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    /* форма внизу */
    .bottom-form {
      position: sticky;
      bottom: 12px;
      z-index: 3;
      padding-top: 10px;
      background: linear-gradient(180deg, rgba(10,10,10,0.0), rgba(7,7,7,0.45));
      margin-top: 20px;
    }
    /* Зменшувати шрифт таблиці при великій кількості рядків */
    @media (max-height: 900px) {
      th, td { font-size: 15px; padding: 8px 10px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- Листочки (тільки кленові) --------------------
leaves_html = ""
for i in range(18):
    left = random.randint(0, 100)
    duration = random.uniform(12, 26)
    delay = random.uniform(0, 12)
    size = random.uniform(20, 44)
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s; font-size:{size}px;">🍁</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

# -------------------- Файл для збереження --------------------
CSV_FILE = "results.csv"
DEFAULT_COLS = ["Місце", "Ім’я", "Клуб", "Вид", "Оцінка", "Додано"]

def load_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            # переконаємося, що всі колонки є
            for c in DEFAULT_COLS:
                if c not in df.columns:
                    df[c] = ""
            return df[DEFAULT_COLS]
        except Exception as e:
            st.error("Не вдалося прочитати файл results.csv: " + str(e))
            return pd.DataFrame(columns=DEFAULT_COLS)
    else:
        # пустий DataFrame із колонками
        return pd.DataFrame(columns=DEFAULT_COLS)

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# -------------------- Заголовок --------------------
st.markdown('<h1 class="app-title">👑 Золота Осінь 2025 🍁</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Турнірна таблиця — вводьте дані внизу. Нові учасниці анімовано підтягуються.</div>', unsafe_allow_html=True)

# -------------------- Завантажити дані --------------------
df = load_data()

# -------------------- Обробка додавання нового рядка через форму внизу --------------------
with st.form("add_form", clear_on_submit=True):
    st.markdown("<div style='display:flex; gap:12px; align-items:center;'>", unsafe_allow_html=True)
    colA, colB, colC, colD, colE = st.columns([1.2, 2.5, 2.5, 1.8, 1.2])
    with colA:
        name = st.text_input("Ім'я", "")
    with colB:
        club = st.text_input("Клуб", "")
    with colC:
        category = st.text_input("Вид", "")
    with colD:
        score = st.text_input("Оцінка (напр. 27.750)", "")
    with colE:
        add_btn = st.form_submit_button("➕ Додати")
    st.markdown("</div>", unsafe_allow_html=True)

# При додаванні — валідація і запис у CSV
if add_btn:
    if not (name and club and category and score):
        st.warning("Заповніть всі поля: Ім'я, Клуб, Вид, Оцінка.")
    else:
        try:
            score_val = float(str(score).replace(",", "."))
            new_row = {
                "Місце": None,
                "Ім’я": name.strip(),
                "Клуб": club.strip(),
                "Вид": category.strip(),
                "Оцінка": score_val,
                "Додано": datetime.utcnow().isoformat()
            }
            df = load_data()  # ще раз підвантажити на випадок паралельного запису
            df = df.append(new_row, ignore_index=True)
            # сортуємо, проставляємо місця
            df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce").fillna(0)
            df = df.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
            df["Місце"] = df.index + 1
            save_data(df)
            # позначимо останнього доданого в сесії для анімації
            st.session_state["last_added"] = name.strip()
            st.experimental_rerun()
        except ValueError:
            st.error("❌ Неправильний формат оцінки. Використовуйте число, наприклад 27.750")

# -------------------- Відобразити таблицю (з анімацією для останнього) --------------------
if not df.empty:
    display_df = df.copy()
    # перетворюємо оцінки для відображення
    display_df["Оцінка"] = display_df["Оцінка"].map(lambda v: ("{:.3f}".format(v)) if pd.notna(v) else "")
    # додамо корону першому
    if len(display_df) >= 1:
        display_df.iloc[0, display_df.columns.get_loc("Ім’я")] = f"👑 <span class='crown'>{display_df.iloc[0]['Ім’я']}</span>"

    # генеруємо HTML-таблицю вручну, щоб додати клас new-row для останнього доданого (за ім'ям)
    l
