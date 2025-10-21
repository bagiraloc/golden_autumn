import streamlit as st
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# Настройка страницы
st.set_page_config(page_title="Золота Осінь 2025 🍂", layout="wide")

# --- Режим отображения ---
mode = st.sidebar.radio("Режим відображення:", ["Суддя", "Екран"])

# --- Ініціалізація даних ---
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Ім'я", "Клуб", "Вид", "Оцінка"])

# --- Функція додавання учасниці ---
def add_participant(name, club, category, score):
    if name and club and category and score:
        new_row = pd.DataFrame(
            [[name.strip().upper(), club.strip(), category.strip(), float(score)]],
            columns=["Ім'я", "Клуб", "Вид", "Оцінка"]
        )
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.session_state.data = st.session_state.data.sort_values(by="Оцінка", ascending=False).reset_index(drop=True)
        st.success(f"✅ Додано: {name}")
    else:
        st.warning("⚠️ Заповни всі поля!")

# --- Функція очищення таблиці ---
def clear_table():
    st.session_state.data = pd.DataFrame(columns=["Ім'я", "Клуб", "Вид", "Оцінка"])
    st.success("🧹 Таблицю очищено!")

# --- Заголовок ---
st.markdown(
    "<h1 style='text-align: center; color: goldenrod;'>Золота Осінь 2025 🍁</h1>",
    unsafe_allow_html=True
)

# --- СУДДЯ ---
if mode == "Суддя":
    st.markdown("### Введення результатів судді")

    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

    with col1:
        name = st.text_input("Ім’я учасниці")
    with col2:
        club = st.text_input("Клуб")
    with col3:
        category = st.text_input("Вид")
    with col4:
        score = st.text_input("Оцінка (наприклад 27.700)")

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("➕ Додати учасницю"):
            add_participant(name, club, category, score)
    with c2:
        if st.button("🧹 Очистити таблицю"):
            clear_table()

    st.markdown("---")

# --- ЕКРАН ---
else:
    st.markdown("### 🏆 Турнірна таблиця (режим екрана)")
    st_autorefresh(interval=10000, limit=None, key="autorefresh")

# --- Відображення таблиці ---
if not st.session_state.data.empty:
    df = st.session_state.data.copy()
    df["Місце"] = range(1, len(df) + 1)
    df = df[["Місце", "Ім'я", "Клуб", "Вид", "Оцінка"]]

    # Анімація плавного з’явлення
    st.markdown(
        """
        <style>
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(10px);}
            to {opacity: 1; transform: translateY(0);}
        }
        div[data-testid="stDataFrame"] {
            animation: fadeIn 0.8s ease-in-out;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        df.style.format({"Оцінка": "{:.3f}"}).set_table_styles(
            [
                {"selector": "th", "props": [("background-color", "#FFD700"), ("color", "black"), ("font-weight", "bold")]},
                {"selector": "td", "props": [("background-color", "#222"), ("color", "#EEE")]},
            ]
        ),
        use_container_width=True,
        height=550,
    )
else:
    st.info("Поки що немає учасниць 👀")

# --- Підпис ---
st.markdown("<p style='text-align:center; color:gray;'>Streamlit версія турнірної таблиці — Золота Осінь 2025</p>", unsafe_allow_html=True)
