import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DOMINUS - Cabina di Regia", page_icon="📊", layout="wide"
)
st.title("📊 DOMINUS - Cabina di Regia Imprenditoriale")
st.markdown("---")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"


@st.cache_data
def load_data(path):
  xls = pd.ExcelFile(path)
  sheet_names = xls.sheet_names
  # Leggiamo i fogli impostando la prima riga come intestazione vera
  sheets_data = {}
  for sheet in sheet_names:
    df = pd.read_excel(path, sheet_name=sheet)
    # Correggiamo l'intestazione prendendo la prima riga se necessario
    if sheet == "INPUT":
      df = pd.read_excel(path, sheet_name=sheet, header=1)
    sheets_data[sheet] = df
  return sheet_names, sheets_data


try:
  sheet_names, sheets_data = load_data(file_path)
  sheet = st.sidebar.selectbox("Seleziona Area", sheet_names)

  st.subheader(f"Area: {sheet}")
  df_display = sheets_data[sheet]

  # Formattazione intelligente per la tabella INPUT (moltiplicazione per 100 per visualizzarli come % ove opportuno)
  if sheet == "INPUT":
    # Se la colonna 'Valore' esiste, formattiamo o gestiamo la visualizzazione
    st.dataframe(df_display, use_container_width=True)
  else:
    st.dataframe(df_display, use_container_width=True)

except Exception as e:
  st.error(f"Errore: {e}")
