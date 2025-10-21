# golden_autumn.py
import streamlit as st
import pandas as pd
import random
import html

# -------------------- Налаштування сторінки --------------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# -------------------- CSS стиль (темна тема) --------------------
# Ми підставимо змінну font_size на основі кількості рядків, щоб "зменшувати" таблицю при великій кількості учасниць.
def make_css(font_size_px=18):
    return f"""
    <style>
    :root {{ --accent: #f6c453; --bg:#0e0e0f; --card:#1a1a1a; --muted:#bfbfbf; }}
    body {{
        background: linear-gradient(180deg, #0d0d0d, #121212);
        color: var(--accent);
        font-family: 'Inter', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }}
    h1 {{
        text-align: center;
        color: var(--accent);
        font-weight: 800;
        text-shadow: 0 0 20px rgba(246,196,83,0.25);
        margin-bottom: 12px;
    }}
    .subtitle {{
        text-align: center;
        color: #e8d8b0;
        margin-bottom: 18px;
    }}
    .top-leaf {{ position: relative; width:100%; text-align:center; font-size:34px; margin-bottom: -12px; }}
    .leaf {{
        position: fixed;
        top: -10vh;
        color: var(--accent);
        opacity: 0.95;
        animation: fall linear infinite;
        z-index: 0;
        pointer-events: none;
        transform-origin: center;
    }}
    @keyframes fall {{
        0% {{ transform: translateY(-10vh) rotate(0deg); opacity: 1; }}
        100% {{ transform: translateY(110vh) rotate(360deg); opacity: 0.9; }}
    }}
    .table-wrap {{
        width: 98%;
        margin: 0 auto 1.5rem auto;
        z-index: 1;
    }}
    table.leaderboard {{
        width: 100%;
        border-collapse: collapse;
        background: rgba(20,20,20,0.85);
        color: var(--accent);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 30px rgba(0,0,0,0.6);
        font-size: {font_size_px}px;
    }}
    table.leaderboard th, table.leaderboard td {{
        padding: 12px 10px;
        text-align: center;
    }}
    table.leaderboard th {{
        background: #222;
        color: var(--accent);
        border-bottom: 2px solid #b8860b;
        font-weight: 700;
    }}
    tr.new-row {{
        animation: slideUp 0.9s ease-out;
    }}
    @keyframes slideUp {{
        from {{ transform: translateY(40px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    .crown {{
        animation: crownPulse 2.5s ease-in-out infinite;
        padding: 0 6px;
    }}
    @keyframes crownPulse {{
        0%,100% {{ text-shadow: 0 0 8px #ffd700; }}
        50% {{ text-shadow: 0 0 20px #ffea00; }}
    }}
    /* input form styling */
    .form-row {{
        display:flex;
        gap:10px;
        justify-content:center;
        align-items:center;
        margin: 18px 0 30px 0;
        flex-wrap:wrap;
    }}
    .stButton>button {{
        background: linear-gradient(90deg, #f6c453, #b8860b);
        color: #1a1a1a !important;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        padding: 8px 14px;
        cursor: pointer;
    }}
    /* small screens */
    @media (max-width: 700px) {{
        table.leaderboard td, table.leaderboard th {{ padding:8px; }}
    }}
    </style>
    """

# -------------------- Листочки (кленовые только) --------------------
def render_leaves(n=16):
    leaves_html = ""
    for i in range(n):
        left = random.randint(0, 95)
        duration = random.uniform(12, 26)
        delay = random.uniform(0, 10)
        size = random.uniform(18, 36)
        leaf = "🍁"  # only maple
        leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s; font-size:{size}px;">{leaf}</div>'
    return leaves_html

# -------------------- Инициализация данных в session_state --------------------
if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
if "last_added" not in st.session_state:
    st.session_state.last_added = None

# -------------------- Логика автообновлення через JS (5 секунд) --------------------
# Вставляємо невидимий HTML, який перезавантажує сторінку кожні 5 секунд
# Якщо це заважає введенню — можна тимчасово прибрати рядок або зменшити інтервал.
auto_refresh_js = """
<script>
const interval = 5000;
setInterval(() => {
    // перезавантажуємо лише якщо фокус не в полі вводу
    if (!document.activeElement || document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        window.location.reload();
    }
}, interval);
</script>
"""
st.components.v1.html(auto_refresh_js, height=0)

# -------------------- Рендер сторінки --------------------
# обчислюємо font-size залежно від кількості рядків (щоб "вміщувати" таблицю)
row_count = len(st.session_state.results)
base_font = 18
if row_count <= 6:
    font_size = base_font
elif row_count <= 12:
    font_size = max(12, base_font - 2)
else:
    font_size = max(10, base_font - min(8, (row_count - 6)//2))

st.markdown(make_css(font_size), unsafe_allow_html=True)
st.markdown(render_leaves(14), unsafe_allow_html=True)

st.markdown("<h1>👑 Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Турнірна таблиця — вводьте дані знизу. Нові учасниці анімовано підтягуються.</div>', unsafe_allow_html=True)

# -------------------- Форма введення внизу (ми покажемо її тут, але вона в стилі "внизу") --------------------
with st.form(key="add_form", clear_on_submit=True):
    c1, c2, c3, c4, c5 = st.columns([3,3,2,2,1])
    name = c1.text_input("Ім'я")
    club = c2.text_input("Клуб")
    category = c3.text_input("Вид")
    score = c4.text_input("Оцінка (наприклад 27.750)")
    add_btn = c5.form_submit_button("➕ Додати")

# -------------------- Додавання учасниці в таблицю --------------------
if add_btn:
    if not name.strip():
        st.error("Введіть ім'я учасниці.")
    else:
        try:
            # якщо порожній рядок для оцінки — ставимо NaN
            score_val = None
            if score and score.strip():
                score_val = float(score.replace(",", "."))
            new_row = {"Місце": None, "Ім’я": name.strip(), "Клуб": club.strip(), "Вид": category.strip(), "Оцінка": score_val}
            # додаємо через concat (append deprecated у нових pandas)
            df = st.session_state.results.copy()
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            # сортуємо (NaN внизу)
            df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")
            df = df.sort_values(by="Оцінка", ascending=False, na_position="last").reset_index(drop=True)
            df["Місце"] = df.index + 1
            st.session_state.results = df
            st.session_state.last_added = name.strip()
            # Щоб побачити зміни негайно (не завжди потрібно) — rerun:
            st.exp
