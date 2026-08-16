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
# CARICA EXCEL
# --------------------------------------------------

@st.cache_resource
def load_wb():
    return load_workbook(
        FILE_XLSX,
        data_only=True
    )

wb = load_wb()

# --------------------------------------------------
# INIZIALIZZA FOGLI
# --------------------------------------------------

if "sheets" not in st.session_state:

    st.session_state.sheets = {}

    for sheet in wb.sheetnames:

        ws = wb[sheet]

        data = []

        for row in ws.iter_rows(values_only=True):
            data.append(list(row))

        df = pd.DataFrame(data)

        df = df.fillna("")

        st.session_state.sheets[sheet] = df

# --------------------------------------------------
# MENU
# --------------------------------------------------

sheet_name = st.sidebar.selectbox(
    "Foglio",
    wb.sheetnames
)

EDITABILI = [
    "ANAGRAFICA",
    "ASSETTO",
    "PATRIMONIO",
    "VALORE",
    "CUSTODIA",
    "LEADER"
]

df = st.session_state.sheets[sheet_name].copy()

# pulizia formule visibili
for col in df.columns:

    df[col] = df[col].apply(
        lambda x: ""
        if str(x).startswith("=")
        else x
    )

for col in df.columns:
    df[col] = df[col].astype(str)

# --------------------------------------------------
# EDITOR
# --------------------------------------------------

if sheet_name in EDITABILI:

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        key=f"editor_{sheet_name}"
    )

else:

    edited_df = df

    st.dataframe(
        edited_df,
        use_container_width=True
    )

st.session_state.sheets[sheet_name] = edited_df

# --------------------------------------------------
# MOTORE DOMINUS
# --------------------------------------------------

def calcola_ambito(df):

    cg_tot = 0
    cg_no = 0

    for _, row in df.iterrows():

        valori = [str(v).strip().upper() for v in row.tolist()]

        risposta = None
        cg = 0

        for i, v in enumerate(valori):

            if v in ["SI", "NO"]:

                risposta = v

                try:
                    cg = float(
                        str(row.iloc[i + 1])
                        .replace(",", ".")
                    )
                except:
                    cg =
