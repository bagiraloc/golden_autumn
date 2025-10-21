import streamlit as st
import pandas as pd
import random

# ---------- Page config ----------
st.set_page_config(page_title="Золота Осінь 2025", layout="wide")

# ---------- Styles (force dark theme + animations) ----------
st.markdown(
    """
<style>
/* Force dark background for Streamlit app container */
.stApp, .css-1dp5vir {
  background-color: #0d0d0d !important;
  color: #f6c453 !important;
}

/* General text / header */
h1 { text-align:center; color:#f6c453; text-shadow:0 0 20px #f6c453; }

/* Leaves */
.leaf {
  position: fixed;
  top: -12vh;
  color: #ffd54f !important;
  font-size: 28px;
  opacity: 0.95;
  animation: fall linear infinite;
  z-index: 0;
}
@keyframes fall {
  0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
  100% { transform: translateY(120vh) rotate(360deg); opacity: 0.08; }
}

/* Table */
.table-wrap { width:100%; overflow:auto; }
.results-table {
  width:100%; border-collapse: collapse; background: rgba(25,25,25,0.95); color:#f6c453;
  box-shadow: 0 8px 30px rgba(0,0,0,0.6); border-radius:12px;
}
.results-table th, .results-table td {
  padding:10px; text-align:center; border-bottom:1px solid rgba(246,196,83,0.08);
}
.results-table th {
  background:#151515; color:#f6c453; font-weight:600; position: sticky; top:0;
}

/* Highlight (new row animation) */
.row-new {
  animation: slideUp 0.9s cubic-bezier(.2,.8,.2,1);
  background: linear-gradient(90deg, rgba(246,196,83,0.06), rgba(246,196,83,0.02));
}
@keyframes slideUp {
  from { transform: translateY(40px); opacity: 0; }
  to   { transform: translateY(0); opacity: 1; }
}

/* Crown animation for leader */
.crown { display:inline-block; animation: crownPulse 2.2s ease-in-out infinite; }
@keyframes crownPulse {
  0%,100% { transform: scale(1); text-shadow: 0 0 10px #ffd54f; }
  50%    { transform: scale(1.12); text-shadow: 0 0 30px #ffea7a; }
}

/* Buttons */
.stButton>button {
  background: linear-gradient(90deg, #f6c453, #b8860b) !important;
  color:#0d0d0d !important; border:none; border-radius:8px; padding:8px 14px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Leaves HTML (gold maple leaves only) ----------
leaves_html = ""
positions = list(range(0, 100, 4))
random.shuffle(positions)
for i, left in enumerate(positions[:28]):
    dur = random.uniform(16, 30)
    delay = random.uniform(0, 12)
    # force maple leaf emoji and gold color
    leaves_html += f'<div class="leaf" style="left:{left}vw; animation-duration:{dur}s; animation-delay:{delay}s">🍁</div>'
st.markdown(leaves_html, unsafe_allow_html=True)

# ---------- Session init ----------
if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame(columns=["Місце", "Прізвище", "Клуб", "Вид", "Оцінка"])
if "last_added" not in st.session_state:
    st.session_state.last_added = None

# ---------- Header ----------
st.markdown("<h1>Золота Осінь 2025</h1>", unsafe_allow_html=True)

# ---------- Admin form (use st.form so submit is reliable) ----------
with st.expander("Панель судді (додавання результатів)", expanded=True):
    with st.form(key="add_form", clear_on_submit=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            fname = st.text_input("Прізвище", key="f_pr")
        with c2:
            club = st.text_input("Клуб", key="f_club")
        with c3:
            event = st.text_input("Вид", key="f_event")
        with c4:
            score_input = st.text_input("Оцінка (напр., 27.750)", key="f_score")
        submit = st.form_submit_button("➕ Додати учасницю")
        clear = st.form_submit_button("🧹 Очистити таблицю", on_click=None)

    # Handle clear as separate button below for reliability
    if st.button("🧹 Очистити таблицю (підтвердження)"):
        st.session_state.results = pd.DataFrame(columns=["Місце", "Прізвище", "Клуб", "Вид", "Оцінка"])
        st.session_state.last_added = None
        st.experimental_rerun()

# ---------- Process submission ----------
if submit:
    # validate inputs
    if not fname or not club or not event or not score_input:
        st.warning("Заповніть всі поля перед додаванням.")
    else:
        # accept comma or dot, preserve 3 decimals
        try:
            val = float(score_input.replace(",", "."))
        except Exception:
            st.error("Неправильний формат оцінки. Використайте число, напр. 27.750")
        else:
            # append row (store score as float)
            new_row = {"Місце": None, "Прізвище": fname.strip(), "Клуб": club.strip(), "Вид": event.strip(), "Оцінка": val}
            st.session_state.results = pd.concat([st.session_state.results, pd.DataFrame([new_row])], ignore_index=True)
            # sort and recalc places
            st.session_state.results["Оцінка"] = st.session_state.results["Оцінка"].astype(float)
            st.session_state.results = st.session_state.results.sort_values(by="Оцінка", ascending=False, ignore_index=True)
            st.session_state.results["Місце"] = range(1, len(st.session_state.results) + 1)
            st.session_state.last_added = fname.strip()
            # clear form fields
            st.session_state["f_pr"] = ""
            st.session_state["f_club"] = ""
            st.session_state["f_event"] = ""
            st.session_state["f_score"] = ""
            st.experimental_rerun()

# ---------- Prepare display dataframe ----------
df_display = st.session_state.results.copy()
if not df_display.empty:
    # ensure formatted display for score (but keep numeric for sorting)
    df_display["Оцінка"] = df_display["Оцінка"].map(lambda x: f"{x:.3f}")
    # mark leader with crown (HTML)
    df_display.loc[0, "Прізвище"] = f"<span class='crown'>👑 {df_display.loc[0, 'Прізвище']}</span>"

# ---------- Render HTML table with animation on last added ----------
if df_display.empty:
    # show empty table header only (no extra text)
    empty_html = """
    <div class="table-wrap">
      <table class="results-table">
        <thead><tr><th>Місце</th><th>Прізвище</th><th>Клуб</th><th>Вид</th><th>Оцінка</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>
    """
    st.markdown(empty_html, unsafe_allow_html=True)
else:
    # build rows with class 'row-new' for last_added
    rows = ""
    for _, r in df_display.iterrows():
        name_for_compare = str(r["Прізвище"]).replace("👑 ", "")
        cls = "row-new" if (st.session_state.last_added and name_for_compare.lower() == st.session_state.last_added.lower()) else ""
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
        f"<tbody>{rows}</tbody>"
        "</table></div>"
    )
    s
