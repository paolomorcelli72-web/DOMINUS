import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DOMINUS - Cabina di Regia", page_icon="📊", layout="wide"
)
st.title("📊 DOMINUS - Gestione e Intervista Interattiva")
st.markdown("---")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"


@st.cache_data
def load_data(path):
  xls = pd.ExcelFile(path)
  sheets_data = {}
  for sheet in xls.sheet_names:
    if sheet == "INPUT":
      # Legge il foglio INPUT usando la seconda riga come intestazione corretta
      df = pd.read_excel(path, sheet_name=sheet, header=1)
    else:
      df = pd.read_excel(path, sheet_name=sheet)
    sheets_data[sheet] = df
  return xls.sheet_names, sheets_data


sheet_names, sheets_data = load_data(file_path)

selected_sheet = st.sidebar.selectbox("Seleziona Sezione", sheet_names)

st.subheader(f"Area Attiva: {selected_sheet}")

df_corrente = sheets_data[selected_sheet].copy()

# Se siamo nel foglio INPUT, trasformiamo la colonna dei valori in percentuale (%)
if selected_sheet == "INPUT" and "Valore" in df_corrente.columns:


  def format_as_percentage(val):
    if pd.notnull(val) and isinstance(val, (int, float)):
      # Moltiplica per 100 e formatta con la virgola e il simbolo %
      val_pct = val * 100
      return f"{val_pct:,.2f}".replace(",", "X").replace(".", ",").replace(
          "X", "."
      ) + "%"
    return val


  df_corrente["Valore"] = df_corrente["Valore"].apply(format_as_percentage)

# Mostriamo la tabella pulita
st.dataframe(df_corrente, use_container_width=True)
