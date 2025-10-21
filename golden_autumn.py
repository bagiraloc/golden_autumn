import streamlit as st
import pandas as pd
import random

# -------------------- Налаштування сторінки --------------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# -------------------- CSS стиль --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #1a1a1a, #0d0d0d);
    color: #f6c453;
    overflow-x: hidden;
}
h1 {
    text-align: center;
    color: #f6c453;
    font-weight: bold;
    text-shadow: 0 0 20px #f6c453;
    margin-bottom: 30px;
}
table {
    width: 100%;
    border-collapse: collapse;
    background: rgba(40,40,40,0.8);
    color: #f6c453;
    border-radius: 12px;
    overflow: hidden;
}
th, td {
    padding: 10px;
    text-align: center;
    font-size: 18px;
}
th {
    background-color: #333;
    color: #f6c453;
    border-bottom: 2px solid #f6c453;
}
tr {
    transition: all 0.7s ease-in-out;
}
tr.new-row {
    animation: fadeSlideIn 1s ease-out;
}
@keyframes fadeSlideIn {
    from { transform: translateY(40px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
button, .stButton>button {
    background: linear-gradient(90deg, #f6c453, #b8860b);
    color: #1a1a1a !important;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    padding: 0.6rem 1.2rem;
    cursor: pointer;
}
button:hover {
    background: linear-gradient(90deg, #ffd700, #f6c453);
}
.leaf {
    position: fixed;
    top: -10vh;
    color: #f6c453;
    opacity: 0.8;
    animation: fall linear infinite;
    z-index: -1;
}
@keyframes fall {
    0% { transform: translateY(0) rotate(0deg); }
    100% { transform: translateY(110vh) rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# -------------------- Листочки --------------------
leaves_html = ""
for i in range(25):
    left = random.randint(0, 100)
    duration = random.uniform(10, 25)
    delay = random.uniform(0, 15)
    size = random.uniform(20, 40)
    leaf = random.choice(["🍁", "🍂", "🍃"])
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s; font-size:{size}px;">{leaf}</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

# -------------------- Таблиця --------------------
if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])

st.markdown("<h1>Золота Осінь 2025 🍂</h1>", unsafe_allow_html=True)

if not st.session_state.results.empty:
    sorted_df = st.session_state.results.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
    sorted_df["Місце"] = sorted_df.index + 1
    # Коронка переможниці
    if not sorted_df.empty:
        sorted_df.iloc[0, 1] = f"👑 {sorted_df.iloc[0, 1]}"
    st.markdown(sorted_df.to_html(index=False, classes="results-table"), unsafe_allow_html=True)
else:
    st.info("Поки що немає учасниць. Додайте першу нижче 👇")

# -------------------- Форма для введення --------------------
with st.expander("🔒 Панель судді", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    name = col1.text_input("Ім’я")
    club = col2.text_input("Клуб")
    category = col3.text_input("Вид")
    score = col4.number_input("Оцінка", min_value=0.0, max_value=60.0, step=0.05)

    add_btn = st.button("➕ Додати учасницю")
    clear_btn = st.button("🧹 Очистити таблицю")

# -------------------- Обробка --------------------
if add_btn and name and club and category:
    new_row = pd.DataFrame([[None, name, club, category, score]], columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
    st.session_state.results = pd.concat([st.session_state.results, new_row], ignore_index=True)
    st.experimental_rerun()

if clear_btn:
    st.session_state.results = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
    st.experimental_rerun()
