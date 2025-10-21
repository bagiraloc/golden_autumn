import streamlit as st
import pandas as pd
import time

# ---- Налаштування сторінки ----
st.set_page_config(page_title="Золота осінь 2025", layout="wide")

# ---- CSS для темного фону, анімацій і листопаду ----
st.markdown(
    """
    <style>
    body { background-color: #0b0b0b; color: #f6c453; overflow: hidden; }
    .leaf { position: fixed; top: -10vh; font-size: 30px; opacity: 0.9;
            animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite; z-index:0; }
    @keyframes fall { 0% {transform: translateY(0) rotate(0deg);} 100% {transform: translateY(120vh) rotate(360deg);} }
    .title { font-size: 48px; text-align: center; color: #f6c453; text-shadow: 0 0 20px #ffda77; margin-bottom: 6px; }
    .subtitle { text-align:center; color:#ffdca8; margin-bottom:18px; }
    .table-wrap { background: rgba(0,0,0,0.45); padding: 12px; border-radius:12px; box-shadow: 0 6px 20px rgba(0,0,0,0.6); }
    table.results { width:100%; border-collapse: collapse; }
    table.results th { color:#f6c453; font-size:18px; padding:8px 6px; text-align:center; }
    table.results td { color:#fff; padding:10px 6px; text-align:center; border-bottom: 1px solid rgba(246,196,83,0.12); }
    .new-row { animation: fadeInUp 0.9s ease; }
    @keyframes fadeInUp { from {opacity:0; transform: translateY(40px);} to {opacity:1; transform:translateY(0);} }
    .controls { margin-bottom:12px; }
    .small-muted { color:#c9b089; font-size:13px; text-align:center; margin-top:6px;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Листя (HTML) ----
leaves_html = ""
for i in range(18):
    left = (i * 7) % 100
    dur = 8 + (i % 6)
    delay = (i % 5) * 0.6
    leaf = ["🍁", "🍂", "🍃"][i % 3]
    leaves_html += f'<div class="leaf" style="left:{left}%; animation-duration:{dur}s; animation-delay:{delay}s">{leaf}</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

# ---- Заголовок ----
st.markdown('<div class="title">🍁 Золота осінь 2025 🍂</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Турнірна таблиця — вводьте оцінки через форму</div>', unsafe_allow_html=True)

# ---- Ініціалізація даних ----
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Місце", "Ім'я", "Клуб", "Вид", "Оцінка"])

# ---- Форма вводу ----
with st.form("add_form", clear_on_submit=True):
    c1, c2, c3, c4, c5 = st.columns([2,3,3,2,1])
    with c1:
        name = st.text_input("Ім'я спортсменки")
    with c2:
        club = st.text_input("Клуб")
    with c3:
        event = st.text_input("Вид (напр., Обруч)")
    with c4:
        score = st.number_input("Оцінка", min_value=0.0, step=0.001, format="%.3f")
    with c5:
        submitted = st.form_submit_button("Додати")
    if submitted and name:
        new_row = {"Місце": None, "Ім'я": name.strip(), "Клуб": club.strip(), "Вид": event.strip(), "Оцінка": float(score)}
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
        st.session_state.data = st.session_state.data.sort_values(by="Оцінка", ascending=False, ignore_index=True)
        st.session_state.data["Місце"] = range(1, len(st.session_state.data) + 1)
        st.success(f"Додано: {name}")
        time.sleep(0.45)

# ---- Фільтр за видом ----
all_events = ["Усі види"] + sorted(set([v for v in st.session_state.data["Вид"].dropna().astype(str).unique() if v!=""]))
sel_event = st.selectbox("Фільтр за видом:", all_events, index=0)
if sel_event == "Усі види":
    display_df = st.session_state.data.copy()
else:
    display_df = st.session_state.data[st.session_state.data["Вид"] == sel_event].reset_index(drop=True)
    display_df["Місце"] = range(1, len(display_df) + 1)

# ---- Підготовка HTML-таблиці з анімацією рядка ----
if not display_df.empty:
    df_for_show = display_df.copy()
    # формат Оцінка вивести з 3 знаками
    df_for_show["Оцінка"] = df_for_show["Оцінка"].map(lambda x: f"{x:.3f}")
    html_table = df_for_show.to_html(classes="results", index=False, escape=False)
    wrapped = f'<div class="table-wrap"><div class="new-row">{html_table}</div></div>'
    st.markdown(wrapped, unsafe_allow_html=True)
else:
    st.info("Поки що немає записів для показу в обраній категорії.")

st.markdown('<div class="small-muted">Таблиця оновлюється одразу після додавання запису</div>', unsafe_allow_html=True)

# ---- Кнопки управління ----
col_reset, col_export = st.columns([1,1])
with col_reset:
    if st.button("🗑️ Очистити таблицю"):
        st.session_state.data = pd.DataFrame(columns=["Місце", "Ім'я", "Клуб", "Вид", "Оцінка"])
        st.experimental_rerun()
with col_export:
    if st.button("⬇️ Експорт CSV"):
        csv = st.session_state.data.to_csv(index=False).encode('utf-8')
        st.download_button("Завантажити CSV", data=csv, file_name="zolota_osin_results.csv", mime="text/csv")