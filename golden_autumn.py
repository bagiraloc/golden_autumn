import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# -------------------- Google Sheets --------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/1S5mf3gVU-FHgOJ_kpfTn02ZzYeXMw0VTfGNX-RL6KMY"

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=30)
def load_data():
    try:
        df = conn.read(spreadsheet=SHEET_URL, usecols=list(range(5)))
        df = df.dropna(how="all")
        df.columns = ["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"]
        return df
    except Exception as e:
        st.error("Помилка при з'єднанні з Google Sheets.")
        st.write(e)
        return pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])

def save_data(df):
    conn.update(spreadsheet=SHEET_URL, data=df)

# -------------------- Стиль --------------------
st.markdown("""
<style>
body { background: linear-gradient(180deg, #0d0d0d, #1a1a1a); color: #f6c453; overflow-x: hidden; }
h1 { text-align: center; color: #f6c453; font-weight: bold; text-shadow: 0 0 25px #f6c453; margin-bottom: 30px; animation: glow 2s ease-in-out infinite alternate; }
@keyframes glow { from { text-shadow: 0 0 15px #f6c453; } to { text-shadow: 0 0 35px #ffd700; } }
table { width: 100%; border-collapse: collapse; background: rgba(30,30,30,0.85); color: #f6c453; border-radius: 12px; overflow: hidden; box-shadow: 0 0 20px rgba(246,196,83,0.2); }
th, td { padding: 10px; text-align: center; font-size: 18px; }
th { background-color: #333; color: #f6c453; border-bottom: 2px solid #f6c453; }
.leaf { position: fixed; top: -10vh; color: #f6c453; opacity: 0.8; animation: fall linear infinite; z-index: -1; }
@keyframes fall { 0% { transform: translateY(0) rotate(0deg); } 100% { transform: translateY(110vh) rotate(360deg); } }
.crown { animation: crownPulse 2.5s ease-in-out infinite; }
@keyframes crownPulse { 0%, 100% { text-shadow: 0 0 10px #ffd700; } 50% { text-shadow: 0 0 25px #ffea00; } }
button, .stButton>button { background: linear-gradient(90deg, #f6c453, #b8860b); color: #1a1a1a !important; border: none; border-radius: 8px; font-weight: bold; padding: 0.6rem 1.2rem; cursor: pointer; }
button:hover { background: linear-gradient(90deg, #ffd700, #f6c453); }
</style>
""", unsafe_allow_html=True)

# -------------------- Листя --------------------
leaves_html = ""
for i in range(25):
    left = random.randint(0, 100)
    duration = random.uniform(15, 30)
    delay = random.uniform(0, 15)
    size = random.uniform(22, 38)
    leaf = random.choice(["🍁", "🍂", "🍃"])
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s; font-size:{size}px;">{leaf}</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

# -------------------- Таблиця --------------------
st.markdown("<h1>Золота Осінь 2025 🍂</h1>", unsafe_allow_html=True)

df = load_data()

with st.expander("🔒 Панель судді", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    name = col1.text_input("Ім’я")
    club = col2.text_input("Клуб")
    category = col3.text_input("Вид")
    score = col4.text_input("Оцінка (наприклад 27.750)")

    col5, col6 = st.columns([1, 1])
    add_btn = col5.button("➕ Додати учасницю")
    clear_btn = col6.button("🧹 Очистити таблицю")

if add_btn:
    if name and club and category and score:
        try:
            score_val = float(score.replace(",", "."))
            new_row = pd.DataFrame([[None, name, club, category, score_val]],
                                   columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
            df = pd.concat([df, new_row], ignore_index=True)
            df["Оцінка"] = df["Оцінка"].astype(float)
            df = df.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
            df["Місце"] = df.index + 1
            save_data(df)
            st.success(f"✅ Учасницю {name} додано!")
            st.rerun()
        except:
            st.error("❌ Помилка у форматі оцінки!")

if clear_btn:
    df = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])
    save_data(df)
    st.warning("🚨 Таблицю очищено!")
    st.rerun()

if not df.empty:
    df.iloc[0, 1] = f"<span class='crown'>👑 {df.iloc[0, 1]}</span>"
    st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)
