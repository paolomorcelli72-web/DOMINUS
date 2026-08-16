import pandas as pd
import streamlit as st

st.set_page_config(page_title="DOMINUS - Cabina di Regia", page_icon="📊", layout="wide")
st.title("📊 DOMINUS - Gestione e Intervista Interattiva")
st.markdown("---")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"

@st.cache_data
def load_data(path):
    xls = pd.ExcelFile(path)
    sheets_data = {}
    for sheet in xls.sheet_names:
        # Se è il foglio INPUT, usiamo la riga 1 come intestazione
        header_row = 1 if sheet == "INPUT" else 0
        df = pd.read_excel(path, sheet_name=sheet, header=header_row)
        sheets_data[sheet] = df
    return xls.sheet_names, sheets_data

sheet_names, sheets_data = load_data(file_path)
selected_sheet = st.sidebar.selectbox("Seleziona Sezione", sheet_names)

st.subheader(f"Area Attiva: {selected_sheet}")

df_to_show = sheets_data[selected_sheet].copy()

# Funzione di formattazione professionale
def format_italian(val, is_pct=False):
    if pd.isnull(val) or not isinstance(val, (int, float)):
        return val
    
    if is_pct:
        # Formattazione per percentuali (es. 0.035 -> 3,50%)
        return f"{val * 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + "%"
    else:
        # Formattazione per migliaia (es. 1234.56 -> 1.234,56)
        return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Applichiamo la logica alle colonne
for col in df_to_show.columns:
    if col == "Valore" and selected_sheet == "INPUT":
        df_to_show[col] = df_to_show[col].apply(lambda x: format_italian(x, is_pct=True))
    elif df_to_show[col].dtype in ['float64', 'int64']:
        df_to_show[col] = df_to_show[col].apply(lambda x: format_italian(x, is_pct=False))

st.dataframe(df_to_show, use_container_width=True)
