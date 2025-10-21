import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

# -------------------- Підключення до Google Sheets --------------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(worksheet="Sheet1")
    df = pd.DataFrame(existing_data)
except Exception as e:
    st.error("❌ Помилка при з'єднанні з Google Sheets")
    st.stop()

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
tr.new-row {
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
    animation: crownPulse 2.5s ease-in-out infinite;
}
@keyframes crownPulse {
    0%, 100% { text-shadow: 0 0 10px #ffd700; }
    50% { text-shadow: 0 0 25px #ffea00; }
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
</style>
""", unsafe_allow_html=True)

# -------------------- Листочки --------------------
leaves_html = ""
for i in range(25):
    left = random.randint(0, 100)
    duration = random.uniform(15, 30)
    delay = random.uniform(0, 15)
    size = random.uniform(22, 38)
    leaf = random.choice(["🍁", "🍂", "🍃"])
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s; font-size:{size}px;">{leaf}</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

# -------------------- Назва --------------------
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

# -------------------- Додавання нової учасниці --------------------
if add_btn:
    if name and club and category and score:
        try:
            score_val = float(score.replace(",", "."))
            new_row = pd.DataFrame([[None, name, club, category, score_val]],
                                   columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])

            # 🟢 Об'єднуємо з існуючими даними
            if not df.empty:
                updated_df = pd.concat([df, new_row], ignore_index=True)
            else:
                updated_df = new_row

            # 🟢 Сортуємо
            updated_df["Оцінка"] = updated_df["Оцінка"].astype(float)
            updated_df = updated_df.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
            updated_df["Місце"] = updated_df.index + 1

            # 🟢 Оновлюємо Google Sheets
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success(f"✅ {name} успішно додана!")
            st.rerun()

        except ValueError:
            st.error("❌ Неправильний формат оцінки! Використовуйте крапку або кому.")

if clear_btn:
    conn.update(worksheet="Sheet1", data=pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"]))
    st.success("🧹 Таблиця очищена!")
    st.rerun()

# -------------------- Відображення --------------------
if not df.empty:
    df = df.copy()
    df = df.dropna(how="all")
    if not df.empty:
        df.iloc[0, 1] = f"<span class='crown'>👑 {df.iloc[0, 1]}</span>"
        st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)
