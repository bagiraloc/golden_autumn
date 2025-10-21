import streamlit as st
import pandas as pd
import random
import gspread
from google.oauth2.service_account import Credentials

# ---------------- Настройки страницы ----------------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# ---------------- Темная стилизация ----------------
st.markdown("""
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
    z-index: -1;
}
@keyframes fall {
    0% { transform: translateY(0) rotate(0deg); }
    100% { transform: translateY(110vh) rotate(360deg); }
}
table {
    width: 100%;
    border-collapse: collapse;
    background: rgba(30,30,30,0.9);
    border-radius: 14px;
    box-shadow: 0 0 20px rgba(246,196,83,0.3);
    font-size: clamp(10px, 1.1vw, 18px);
}
th, td {
    padding: 6px;
    text-align: center;
    color: #f6c453;
    word-break: break-word;
}
th {
    background-color: #1e1e1e;
    border-bottom: 2px solid #f6c453;
}
tr.highlight {
    animation: slideUp 0.8s ease-out;
}
@keyframes slideUp {
    from { transform: translateY(50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
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
    color: #0d0d0d !important;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    padding: 0.6rem 1.2rem;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #ffd700, #f6c453);
}
.scroll-container {
    max-height: 80vh;
    overflow-y: auto;
    scrollbar-width: thin;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Листочки ----------------
leaves_html = ""
for i in range(25):
    left = random.randint(0, 100)
    duration = random.uniform(15, 30)
    delay = random.uniform(0, 25)
    leaf = random.choice(["🍁", "🍂", "🍁"])
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s;">{leaf}</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

# ---------------- Подключение Google Sheets ----------------
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPE)
client = gspread.authorize(creds)

SPREADSHEET_ID = "1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY"
SHEET_NAME = "Аркуш1"  # или то имя, которое ты реально видишь внизу в таблице
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# ---------------- Загрузка таблицы ----------------
def load_results():
    data = sheet.get_all_records()
    if not data:
        return pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
    df = pd.DataFrame(data)
    df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")
    df = df.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
    df["Місце"] = df.index + 1
    return df

# ---------------- Добавление участницы ----------------
def add_participant(name, club, event, score):
    sheet.append_row([name, club, event, score])

# ---------------- Интерфейс ----------------
st.markdown("<h1>Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)

with st.expander("Панель судді", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    name = c1.text_input("Ім’я")
    club = c2.text_input("Клуб")
    event = c3.text_input("Вид")
    score = c4.text_input("Оцінка (наприклад 27.700)")

    colA, colB = st.columns([1,1])
    add_btn = colA.button("➕ Додати учасницю")
    refresh_btn = colB.button("🔄 Оновити турнірку")

if add_btn:
    if name and club and event and score:
        try:
            score_val = float(score.replace(",", "."))
            add_participant(name, club, event, score_val)
            st.success(f"✅ {name} додана до турнірки!")
        except ValueError:
            st.error("⚠️ Перевір формат оцінки!")
    else:
        st.warning("⚠️ Заповни всі поля!")

# ---------------- Отображение таблицы ----------------
df = load_results()

if not df.empty:
    df["Оцінка"] = df["Оцінка"].map(lambda x: f"{x:.3f}")
    df.iloc[0, 1] = f"<span class='crown'>👑 {df.iloc[0, 1]}</span>"

    html = "<div class='scroll-container'><table><thead><tr>" + "".join([f"<th>{col}</th>" for col in df.columns]) + "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += f"<tr>" + "".join([f"<td>{x}</td>" for x in row.values]) + "</tr>"
    html += "</tbody></table></div>"

    st.markdown(html, unsafe_allow_html=True)
else:
    st.info("Поки що немає учасниць.")
