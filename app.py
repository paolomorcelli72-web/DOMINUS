import pandas as pd
import streamlit as st

st.set_page_config(page_title="DOMINUS", layout="wide")
st.title("📊 DOMINUS - Cabina di Regia")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"


# Carica i fogli leggendo direttamente il percorso del file
@st.cache_data
def load_data(path):
  xls = pd.ExcelFile(path)
  sheet_names = xls.sheet_names
  # Leggiamo tutti i fogli in un dizionario di DataFrame (oggetti perfettamente serializzabili)
  sheets_data = {sheet: pd.read_excel(path, sheet_name=sheet) for sheet in sheet_names}
  return sheet_names, sheets_data


try:
  sheet_names, sheets_data = load_data(file_path)
  sheet = st.sidebar.selectbox("Seleziona Area", sheet_names)
  st.subheader(f"Area: {sheet}")
  st.dataframe(sheets_data[sheet], use_container_width=True)
except Exception as e:
  st.error(f"Errore: {e}")
