import streamlit as st
import pandas as pd
import random

# -------------------- Налаштування сторінки --------------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# -------------------- CSS стиль --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #0d0d0d, #1a1a1a);
    color: #f6c453;
    overflow-x: hidden;
}
h1 {
    text-align: center;
    color: #f6c453;
    font-weight: bold;
    text-shadow: 0 0 25px #f6c453;
    margin-bottom: 30px;
    animation: glow 2s ease-in-out infinite alternate;
}
@keyframes glow {
    from { text-shadow: 0 0 15px #f6c453; }
    to { text-shadow: 0 0 35px #ffd700; }
}
table {
    width: 100%;
    border-collapse: collapse;
    background: rgba(30,30,30,0.85);
    color: #f6c453;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(246,196,83,0.2);
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
tr.highlight {
    animation: slideUp 0.8s ease-out;
}
@keyframes slideUp {
    from { transform: translateY(60px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
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
.crown {
    animation: crownPulse 3s ease-in-out infinite;
}
@keyframes crownPulse {
    0%, 100% { text-shadow: 0 0 10px #ffd700; }
    50% { text-shadow: 0 0 25px #ffea00; }
}
.stButton>button {
    background: linear-gradient(90deg, #f6c453, #b8860b);
    color: #1a1a1a !important;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    padding: 0.6rem 1.2rem;
    cursor: pointer;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #ffd700, #f6c453);
}
</style>
""", unsafe_allow_html=True)

# -------------------- Анімація листочків (постійна) --------------------
leaves_html = ""
for i in range(35):
    left = random.randint(0, 100)
    duration = random.uniform(15, 30)
    delay = random.uniform(0, 25)
    size = random.uniform(22, 38)
    leaf = random.choice(["🍁", "🍂", "🍃"])
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s; font-size:{size}px;">{leaf}</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

# -------------------- Таблиця --------------------
if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
if "last_added" not in st.session_state:
    st.session_state.last_added = None

st.markdown("<h1>Золота Осінь 2025 🍂</h1>", unsafe_allow_html=True)

# -------------------- Панель судді --------------------
with st.expander("🔒 Панель судді", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    name = col1.text_input("Ім’я")
    club = col2.text_input("Клуб")
    category = col3.text_input("Вид")
    score = col4.text_input("Оцінка (наприклад 27.750)")

    col5, col6 = st.columns([1, 1])
    add_btn = col5.button("➕ Додати учасницю", key="add")
    clear_btn = col6.button("🧹 Очистити таблицю", key="clear")

# -------------------- Логіка --------------------
if add_btn:
    if name and club and category and score:
        try:
            score_val = float(score.replace(",", "."))
            new_row = pd.DataFrame([[None, name, club, category, f"{score_val:.3f}"]],
                                   columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
            st.session_state.results = pd.concat([st.session_state.results, new_row], ignore_index=True)
            st.session_state.results["Оцінка"] = st.session_state.results["Оцінка"].astype(float)
            st.session_state.results = st.session_state.results.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
            st.session_state.results["Місце"] = st.session_state.results.index + 1
            st.session_state.last_added = name
        except ValueError:
            st.error("❌ Неправильний формат оцінки! Використовуйте крапку або кому.")

if clear_btn:
    st.session_state.results = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
    st.session_state.last_added = None

# -------------------- Відображення --------------------
if not st.session_state.results.empty:
    df = st.session_state.results.copy()
    df.iloc[0, 1] = f"<span class='crown'>👑 {df.iloc[0, 1]}</span>"

    html = "<table><thead><tr>" + "".join([f"<th>{c}</th>" for c in df.columns]) + "</tr></thead><tbody>"
    for _, row in df.iterrows():
        cls = "highlight" if row["Ім’я"].replace("👑 ", "") == st.session_state.last_added else ""
        html += "<tr class='{0}'>" + "".join([f"<td>{x}</td>" for x in row.values]) + "</tr>".format(cls)
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)
