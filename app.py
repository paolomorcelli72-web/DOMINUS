
# -----------------------------
# AGGIORNA SESSIONE
# -----------------------------

st.session_state.sheets[sheet_name] = edited_df

# -----------------------------
# CALCOLO DOMINUS
# -----------------------------

def trova_colonna(df, testo):

    for c in range(len(df.columns)):

        for r in range(min(5, len(df))):

            val = str(df.iloc[r, c]).strip().upper()

            if testo.upper() in val:
                return c

    return None


def calcola_ambito(df):

    risposta_col = trova_colonna(df, "RISPOSTA")
    cg_col = trova_colonna(df, "CG")

    if risposta_col is None or cg_col is None:
        return 0

    cg_tot = 0
    cg_no = 0

    for r in range(1, len(df)):

        risposta = str(
            df.iloc[r, risposta_col]
        ).strip().upper()

        try:
            cg = float(
                str(
                    df.iloc[r, cg_col]
                ).replace(",", ".")
            )
        except:
            cg = 0

        cg_tot += cg

        if risposta == "NO":
            cg_no += cg

    if cg_tot == 0:
        return 0

    return cg_no / cg_tot


assetto = calcola_ambito(
    st.session_state.sheets["ASSETTO"]
)

patrimonio = calcola_ambito(
    st.session_state.sheets["PATRIMONIO"]
)

valore = calcola_ambito(
    st.session_state.sheets["VALORE"]
)

custodia = calcola_ambito(
    st.session_state.sheets["CUSTODIA"]
)

dominus_score = round(
    (
        assetto * 50 +
        patrimonio * 10 +
        valore * 30 +
        custodia * 10
    ),
    2
)

st.divider()

st.subheader("📈 DOMINUS SCORE LIVE")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Assetto",
    f"{assetto*100:.2f}%"
)

c2.metric(
    "Patrimonio",
    f"{patrimonio*100:.2f}%"
)

c3.metric(
    "Valore",
    f"{valore*100:.2f}%"
)

c4.metric(
    "Custodia",
    f"{custodia*100:.2f}%"
)

c5.metric(
    "Score",
    f"{dominus_score:.2f}"
)

if dominus_score < 35:
    rating = "AAA"
elif dominus_score < 43:
    rating = "AA"
elif dominus_score < 50:
    rating = "A"
elif dominus_score < 58:
    rating = "BBB"
elif dominus_score < 65:
    rating = "BB"
elif dominus_score < 80:
    rating = "B"
else:
    rating = "D"

st.success(f"🏆 Rating: {rating}")

# -----------------------------
# SALVATAGGIO
# -----------------------------

if st.button("💾 Salva Workbook"):

    wb_save = load_workbook(FILE_XLSX)

    for foglio, dataframe in st.session_state.sheets.items():

        ws = wb_save[foglio]

        max_r = min(
            len(dataframe),
            ws.max_row
        )

        max_c = min(
            len(dataframe.columns),
            ws.max_column
        )

        for r in range(max_r):

            for c in range(max_c):

                valore = dataframe.iat[r, c]

                if pd.isna(valore):
                    valore = None

                ws.cell(
                    row=r + 1,
                    column=c + 1,
                    value=valore
                )

    wb_save.save(FILE_XLSX)

    st.success("✅ Workbook salvato")
