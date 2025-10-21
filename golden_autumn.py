import streamlit as st
import pandas as pd
import time
from streamlit.components.v1 import html

# ---- Налаштування сторінки ----
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# ---- CSS стиль ----
st.markdown("""
<style>
body {background-color:#0e0e0e; color:#ffd700; overflow:hidden;}
h1, h2, h3 {color:#ffd700; text-align:center;}
.table-container {max-height:80vh; overflow:auto; margin-top:20px;}
table {width:100%; border-collapse:collapse; font-size:18px;}
th, td {border-bottom:1px solid #555; padding:8px; text-align:center;}
tr:nth-child(1) {color:#ffdd33; font-weight:bold; font-size:20px;}

@keyframes fall {
  0% {transform:translateY(-10vh); opacity:1;}
  100% {transform:translateY(110vh); opacity:0;}
}
.leaf {
  position:fixed;
  top:-10vh;
  font-size:30px;
  opacity:0.8;
  color:#ffd700;
  animation-name:fall;
  animation-timing-function:linear;
}
@keyframes crown {
  0%, 100% {transform:scale(1);}
  50% {transform:scale(1.2);}
}
.crown {
  display:inline-block;
  animation:crown 2s infinite;
  color:#ffcc00;
}
</style>
""", unsafe_allow_html=True)

# ---- Листочки ----
leaves_html = ""
for i in range(15):
    left = i * 6
    duration = 6 + (i % 3)
    delay = i * 2
    leaves_html += f'<div class="leaf" style="left:{left}%; animation-duration:{duration}s; animation-delay:{delay}s;">🍁</div>'
html(leaves_html, height=0)

# ---- Назва ----
st.markdown("<h1>Золота Осінь 2025</h1>", unsafe_allow_html=True)

# ---- Ініціалізація ----
if "gymnasts" not in st.session_state:
    st.session_state.gymnasts = []

# ---- Таблиця ----
if len(st.session_state.gymnasts) > 0:
    df = pd.DataFrame(st.session_state.gymnasts, columns=["Ім'я", "Клуб", "Вид", "Оцінка"])
    df["Оцінка"] = pd.to_numeric(df["Оцінка"], errors="coerce")
    df = df.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    df.index.name = "Місце"
    
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Анімація для 1 місця ----
    top_name = df.iloc[0]["Ім'я"]
    crown_html = f"""
    <script>
    setInterval(() => {{
      const el = window.parent.document.querySelector('table tbody tr:first-child td:first-child');
      if(el && !el.querySelector('.crown')) {{
        el.innerHTML = '👑 <span class="crown">{top_name}</span>';
      }}
    }}, 25000);
    </script>
    """
    html(crown_html, height=0)

# ---- Панель введення (внизу сторінки) ----
with st.container():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### ➕ Додати учасницю")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        name = st.text_input("Ім'я")
    with col2:
        club = st.text_input("Клуб")
    with col3:
        event = st.text_input("Вид")
    with col4:
        score = st.text_input("Оцінка")

    add = st.button("Додати")
    clear = st.button("Очистити таблицю")

    if add and name and score:
        st.session_state.gymnasts.append([name, club, event, score])
        st.rerun()

    if clear:
        st.session_state.gymnasts = []
        st.rerun()
