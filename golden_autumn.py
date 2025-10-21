 " + str(df.iloc[0]["Ім'я"])
    except Exception:
        pass

# 📊 Отображаем таблицу
st.markdown(
    df.to_html(index=False, escape=False),
    unsafe_allow_html=True
)

# 🔁 Автообновление
st.markdown("<p style='text-align:center; color:gray;'>⏳ Оновлення кожні 5 секунд</p>", unsafe_allow_html=True)
time.sleep(5)
st.experimental_rerun()

# 🧾 Форма добавления данных (внизу страницы)
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("➕ Додати учасницю")

with st.form("add_participant", clear_on_submit=True):
    place = st.text_input("Місце")
    name = st.text_input("Ім'я")
    club = st.text_input("Клуб")
    apparatus = st.text_input("Вид")
    score = st.text_input("Оцінка")

    submitted = st.form_submit_button("Додати")

    if submitted:
        if name:
            new_row = pd.DataFrame([[place, name, club, apparatus, score]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            conn.update(worksheet="Аркуш1", data=df)
            st.success(f"✅ Учасницю {name} додано!")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.warning("⚠️ Введіть ім'я учасниці перед збереженням.")
