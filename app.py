import streamlit as st
import pandas as pd
from openpyxl import load_workbook

FILE = "DOMINUS 2026 DEFINITIVO.xlsx"

st.set_page_config(
    page_title="DOMINUS 2026",
    layout="wide"
)

st.title("📊 DOMINUS WEB ENGINE")

# --------------------------------------------------
# LOAD EXCEL
# --------------------------------------------------
@st.cache_resource
def load_excel():
    return load_workbook(FILE)

wb = load_excel()

# --------------------------------------------------
# SHEETS
# --------------------------------------------------
sheet_names = wb.sheetnames

selected_sheet = st.sidebar.selectbox(
    "Seleziona Foglio",
    sheet_names
)

ws = wb[selected_sheet]

# --------------------------------------------------
# EXCEL --> DATAFRAME
# --------------------------------------------------
data = []

for row in ws.iter_rows(values_only=True):
    r = []

    for cell in row:
        if cell is None:
            r.append("")
        else:
            r.append(str(cell))

    data.append(r)

if len(data) == 0:
    df = pd.DataFrame()
else:
    df = pd.DataFrame(data)

# --------------------------------------------------
# FORCE TEXT (NO CHECKBOX)
# --------------------------------------------------
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
    column_config=column_config
)

# --------------------------------------------------
# SAVE
# --------------------------------------------------
if st.button("💾 Salva"):

    wb_save = load_workbook(FILE)

    ws_save = wb_save[selected_sheet]

    for r in range(len(edited_df)):
        for c in range(len(edited_df.columns)):

            value = edited_df.iat[r, c]

            if value == "":
                value = None

            ws_save.cell(
                row=r + 1,
                column=c + 1
            ).value = value

    wb_save.save(FILE)

    st.success("Salvataggio completato")

# --------------------------------------------------
# DOMINUS SCORE
# --------------------------------------------------
def calcola_ambito(nome_foglio):

    ws = wb[nome_foglio]

    cg_tot = 0
    cg_no = 0

    si = 0
    no = 0

    for row in ws.iter_rows(min_row=2):

        risposta = str(row[2].value).strip().upper()

        try:
            cg = float(row[3].value)
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

    totale = si + no

    score = 0

    if totale > 0:
        score = si / totale

    return {
        "si": si,
        "no": no,
        "vulnerabilita": vulnerabilita,
        "score": score
    }

# --------------------------------------------------
# SCORE LIVE
# --------------------------------------------------
try:

    assetto = calcola_ambito("ASSETTO")
    patrimonio = calcola_ambito("PATRIMONIO")
    valore = calcola_ambito("VALORE")
    custodia = calcola_ambito("CUSTODIA")

    score_finale = (
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
        "Dominus Score",
        f"{score_finale:.2f}"
    )

    if score_finale < 35:
        rating = "AAA"
    elif score_finale < 43:
        rating = "AA"
    elif score_finale < 50:
        rating = "A"
    elif score_finale < 58:
        rating = "BBB"
    elif score_finale < 65:
        rating = "BB"
    elif score_finale < 80:
        rating = "B"
    else:
        rating = "D"

    st.success(f"🏆 Rating: {rating}")

except Exception:
    pass
