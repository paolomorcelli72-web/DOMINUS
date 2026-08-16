import streamlit as st
import pandas as pd
from openpyxl import load_workbook

FILE_XLSX = "DOMINUS 2026 DEFINITIVO.xlsx"

st.set_page_config(
    page_title="DOMINUS WEB",
    layout="wide"
)

st.title("📊 DOMINUS WEB")

# --------------------------------------------------
# CARICA EXCEL UNA SOLA VOLTA
# --------------------------------------------------
@st.cache_resource
def load_excel():
    return load_workbook(FILE_XLSX, data_only=False)

wb = load_excel()

# --------------------------------------------------
# CREA DATAFRAME IN MEMORIA
# --------------------------------------------------
if "sheets" not in st.session_state:

    st.session_state.sheets = {}

    for sheet in wb.sheetnames:

        ws = wb[sheet]

        rows = []

        for row in ws.iter_rows(values_only=True):
            rows.append(list(row))

        st.session_state.sheets[sheet] = pd.DataFrame(rows)

# --------------------------------------------------
# MENU
# --------------------------------------------------
sheet_name = st.sidebar.selectbox(
    "Foglio",
    wb.sheetnames
)

df = st.session_state.sheets[sheet_name]

# tutto testo
for col in df.columns:
    df[col] = df[col].astype(str)

column_config = {
    col: st.column_config.TextColumn(
        str(col)
    )
    for col in df.columns
}

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    column_config=column_config,
    key=f"editor_{sheet_name}"
)

# aggiorna memoria
st.session_state.sheets[sheet_name] = edited_df

# --------------------------------------------------
# MOTORE DOMINUS
# --------------------------------------------------
def calcola_ambito(df):

    cg_tot = 0
    cg_no = 0

    si = 0
    no = 0

    for i in range(1, len(df)):

        try:
            risposta = str(df.iloc[i, 2]).strip().upper()
        except:
            continue

        try:
            cg = float(
                str(df.iloc[i, 3]).replace(",", ".")
            )
        except:
            cg = 0

        cg_tot += cg

        if risposta == "SI":
            si += 1

        elif risposta == "NO":
            no += 1
            cg_no += cg

    vulnerabilita = 0

    if cg_tot > 0:
        vulnerabilita = cg_no / cg_tot

    return {
        "si": si,
        "no": no,
        "cg_tot": cg_tot,
        "cg_no": cg_no,
        "vulnerabilita": vulnerabilita
    }

# --------------------------------------------------
# CALCOLO LIVE
# --------------------------------------------------
try:

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

    dominus_score = (
        assetto["vulnerabilita"] * 50 +
        patrimonio["vulnerabilita"] * 10 +
        valore["vulnerabilita"] * 30 +
        custodia["vulnerabilita"] * 10
    ) * 100

    st.divider()

    st.subheader("📈 DOMINUS SCORE LIVE")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Assetto",
        f"{assetto['vulnerabilita']*100:.2f}%"
    )

    c2.metric(
        "Patrimonio",
        f"{patrimonio['vulnerabilita']*100:.2f}%"
    )

    c3.metric(
        "Valore",
        f"{valore['vulnerabilita']*100:.2f}%"
    )

    c4.metric(
        "Custodia",
        f"{custodia['vulnerabilita']*100:.2f}%"
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

except Exception as e:
    st.error(f"Errore motore DOMINUS: {e}")

# --------------------------------------------------
# SALVATAGGIO
# --------------------------------------------------
if st.button("💾 Salva Workbook"):

    wb_save = load_workbook(FILE_XLSX)

    for foglio, dataframe in st.session_state.sheets.items():

        ws = wb_save[foglio]

        for r in range(len(dataframe)):
            for c in range(len(dataframe.columns)):

                valore = dataframe.iat[r, c]

                if valore == "nan":
                    valore = None

                ws.cell(
                    row=r + 1,
                    column=c + 1
                ).value = valore

    wb_save.save(FILE_XLSX)

    st.success("✅ File salvato")
