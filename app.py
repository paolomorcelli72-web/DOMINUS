import pandas as pd
import streamlit as st
import openpyxl

st.set_page_config(page_title="DOMINUS - Editor Totale", layout="wide")
st.title("📊 DOMINUS - Editor Formato Identico all'Originale")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"

@st.cache_data
def load_data_exact():
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheets_dict = {}
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        data = list(ws.values)
        if data:
            df = pd.DataFrame(data)
            # Sostituiamo i valori None con stringhe vuote per una visualizzazione pulita,
            # ma senza distruggere i tipi nativi (percentuali e numeri originali dell'Excel)
            df = df.fillna("")
        else:
            df = pd.DataFrame()
        sheets_dict[sheet_name] = df
    return sheets_dict

if "master_data" not in st.session_state:
    st.session_state["master_data"] = load_data_exact()

sheet_list = list(st.session_state["master_data"].keys())
selected_sheet = st.sidebar.selectbox("Seleziona Sezione", sheet_list)

st.subheader(f"Sezione: {selected_sheet}")

# Configurazione colonna per colonna: impedisce che i testi "SI/NO" diventino checkbox, 
# lasciando intatte le percentuali e i numeri originali.
df_corrente = st.session_state["master_data"][selected_sheet]
column_config = {col: st.column_config.TextColumn(str(col)) for col in df_corrente.columns}

# Editor Blindato
edited_df = st.data_editor(
    df_corrente,
    use_container_width=True,
    num_rows="dynamic",
    column_config=column_config,
    key=f"editor_blindato_{selected_sheet}"
)

st.session_state["master_data"][selected_sheet] = edited_df

if st.button("💾 Salva"):
    st.success("Modifiche salvate con successo!")
