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
  sheets_data = {
      sheet: pd.read_excel(path, sheet_name=sheet) for sheet in xls.sheet_names
  }
  return xls.sheet_names, sheets_data


sheet_names, sheets_data = load_data(file_path)

selected_sheet = st.sidebar.selectbox("Seleziona Sezione", sheet_names)

st.subheader(f"Area Attiva: {selected_sheet}")

df_corrente = sheets_data[selected_sheet]


# Funzione per formattare i numeri con punti e virgole all'italiana
def format_to_italian(val):
  if isinstance(val, (int, float)):
    # Formatta con separatore delle migliaia (punto) e decimali (virgola)
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
  return val


# Applichiamo la formattazione visiva alle colonne numeriche
df_visivo = df_corrente.copy()
for col in df_visivo.select_dtypes(include=["number"]).columns:
  df_visivo[col] = df_visivo[col].apply(format_to_italian)

# Mostriamo la tabella
st.dataframe(df_visivo, use_container_width=True)
