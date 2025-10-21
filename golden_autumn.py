import streamlit as st  
import pandas as pd  
import random  

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
</style>  
""", unsafe_allow_html=True)  

# ---------------- Листочки ----------------  
leaves_html = ""  
for i in range(25):  
    left = random.randint(0, 100)  
    duration = random.uniform(15, 30)  
    delay = random.uniform(0, 25)  
    leaf = random.choice(["🍁", "🍁", "🍂", "🍁"])  
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{duration}s; animation-delay:{delay}s;">{leaf}</div>'  
st.markdown(leaves_html, unsafe_allow_html=True)  

# ---------------- Состояние таблицы ----------------  
if "results" not in st.session_state:  
    st.session_state.results = pd.DataFrame(columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])  
if "last_added" not in st.session_state:  
    st.session_state.last_added = None  

st.markdown("<h1>Золота Осінь 2025 🍁</h1>", unsafe_allow_html=True)  

# ---------------- Панель судьи ----------------  
with st.expander("Панель судді", expanded=True):  
    c1, c2, c3, c4 = st.columns(4)  
    name = c1.text_input("Ім’я")  
    club = c2.text_input("Клуб")  
    event = c3.text_input("Вид")  
    score = c4.text_input("Оцінка (наприклад 27.700)")  

    colA, colB = st.columns([1,1])  
    add_btn = colA.button("➕ Додати учасницю")  
    clear_btn = colB.button("🧹 Очистити таблицю")  

# ---------------- Добавление участницы ----------------  
if add_btn:  
    if name and club and event and score:  
        try:  
            score_val = float(score.replace(",", "."))  
            new_row = pd.DataFrame([[None, name, club, event, score_val]],  
                                   columns=["Місце", "Ім’я", "Клуб", "Вид", "Оцінка"])  
            st.session
