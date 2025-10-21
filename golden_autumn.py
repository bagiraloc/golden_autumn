import streamlit as st
import pandas as pd
import random

# ---------- Page config ----------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# ---------- Styles ----------
st.markdown(
    """
<style>
.stApp {
  background-color: #0d0d0d !important;
  color: #f6c453 !important;
}
h1 {
  text-align:center;
  color:#f6c453;
  text-shadow:0 0 20px #f6c453;
}
.leaf {
  position: fixed;
  top: -12vh;
  color: #ffd54f !important;
  font-size: 28px;
  opacity: 0.9;
  animation: fall linear infinite;
  z-index: 0;
}
@keyframes fall {
  0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
  100% { transform: translateY(120vh) rotate(360deg); opacity: 0.1; }
}
.table-wrap { width:100%; overflow:auto; }
.results-table {
  width:100%; border-collapse: collapse;
  background: rgba(25,25,25,0.95);
  color:#f6c453;
  box-shadow: 0 8px 30px rgba(0,0,0,0.6);
  border-radius:12px;
}
.results-table th, .results-table td {
  padding:10px; text-align:center;
  border-bottom:1px solid rgba(246,196,83,0.08);
}
.results-table th {
  background:#151515; color:#f6c453; font-weight:600;
}
.row-new {
  animation: slideUp 0.9s cubic-bezier(.2,.8,.2,1);
  background: rgba(246,196,83,0.05);
}
@keyframes slideUp {
  from { transform: translateY(40px); opacity: 0; }
  to   { transform: translateY(0); opacity: 1; }
}
.crown {
  display:inline-block;
  animation: crownPulse 2.2s ease-in-out infinite;
}
@keyframes crownPulse {
  0%,100% { transform: scale(1); text-shadow: 0 0 10px #ffd54f; }
  50%    { transform: scale(1.12); text-shadow: 0 0 30px #ffea7a; }
}
.stButton>button {
  background: linear-gradient(90deg, #f6c453, #b8860b) !important;
  color:#0d0d0d !important; border:none; border-radius:8px; padding:8px 14px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Leaves ----------
leaves_html = ""
for i in range(28):
    left = random.randint(0, 100)
    dur = random.uniform(16, 30)
    delay = random.uniform(0, 20)
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{dur}s; animation-delay:{delay}s;">🍁</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

# ---------- Session init ----------
if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame(columns=["Місце", "Прізвище", "Клуб", "Вид", "Оцінка"])
if "last_added" not in st.session_state:
    st.session_state.last_added = None

# ---------- Header ----------
st.markdown("<h1>Золота Осінь 2025</h1>", unsafe_allow_html=True)

# ---------- Admin form ----------
with st.expander("Панель судді (додавання результатів)", expanded=True):
    with st.form("add_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        fname = c1.text_input("Прізвище")
        club = c2.text_input("Клуб")
        event = c3.text_input("Вид")
        score_input = c4.text_input("Оцінка (напр., 27.750)")

        submit = st.form_submit_button("➕ Додати учасницю")
        clear = st.form_submit_button("🧹 Очистити таблицю")

    # Очищення всієї таблиці
    if clear:
        st.session_state.results = pd.DataFrame(columns=["Місце", "Прізвище", "Клуб", "Вид", "Оцінка"])
        st.session_state.last_added = None
        st.success("Таблицю очищено!")

# ---------- Обробка додавання ----------
if submit:
    if not fname or not club or not event or not score_input:
        st.warning("Заповніть всі поля перед додаванням.")
    else:
        try:
            val = float(score_input.replace(",", "."))
            new_row = {"Місце": None, "Прізвище": fname.strip(), "Клуб": club.strip(), "Вид": event.strip(), "Оцінка": val}
            st.session_state.results = pd.concat([st.session_state.results, pd.DataFrame([new_row])], ignore_index=True)
            st.session_state.results["Оцінка"] = st.session_state.results["Оцінка"].astype(float)
            st.session_state.results = st.session_state.results.sort_values(by="Оцінка", ascending=False, ignore_index=True)
            st.session_state.results["Місце"] = range(1, len(st.session_state.results) + 1)
            st.session_state.last_added = fname.strip()
            st.success(f"✅ Учасницю {fname} додано!")
        except ValueError:
            st.error("Неправильний формат оцінки. Використайте число, напр. 27.750")

# ---------- Відображення таблиці ----------
df_display = st.session_state.results.copy()
if not df_display.empty:
    df_display["Оцінка"] = df_display["Оцінка"].map(lambda x: f"{x:.3f}")
    df_display.loc[0, "Прізвище"] = f"<span class='crown'>👑 {df_display.loc[0, 'Прізвище']}</span>"

    rows = ""
    for _, r in df_display.iterrows():
        cls = "row-new" if (st.session_state.last_added and str(r["Прізвище"]).replace('👑 ','').lower() == st.session_state.last_added.lower()) else ""
        rows += (
            f"<tr class='{cls}'>"
            f"<td>{int(r['Місце'])}</td>"
            f"<td>{r['Прізвище']}</td>"
            f"<td>{r['Клуб']}</td>"
            f"<td>{r['Вид']}</td>"
            f"<td>{r['Оцінка']}</td>"
            f"</tr>"
        )

    table_html = (
        "<div class='table-wrap'>"
        "<table class='results-table'>"
        "<thead><tr><th>Місце</th><th>Прізвище</th><th>Клуб</th><th>Вид</th><th>Оцінка</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.markdown(
        """
        <div class="table-wrap">
          <table class="results-table">
            <thead><tr><th>Місце</th><th>Прізвище</th><th>Клуб</th><th>Вид</th><th>Оцінка</th></tr></thead>
            <tbody></tbody>
          </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Корона "пульсує" кожні 25 секунд ----------
st.markdown(
    """
<script>
setInterval(()=>{
  const c = document.querySelector('.crown');
  if(c){
    c.style.transform = 'scale(1.15)';
    setTimeout(()=>{ c.style.transform = 'scale(1)'; }, 1000);
  }
}, 25000);
</script>
""",
    unsafe_allow_html=True,
)
