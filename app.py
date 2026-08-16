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
    header_row = 1 if sheet == "INPUT" else 0
    df = pd.read_excel(path, sheet_name=sheet, header=header_row)
    sheets_data[sheet] = df
  return xls.sheet_names, sheets_data


sheet_names, sheets_data = load_data(file_path)
selected_sheet = st.sidebar.selectbox("Seleziona Sezione", sheet_names)

st.subheader(f"Area Attiva: {selected_sheet}")

df_to_show = sheets_data[selected_sheet].copy()


# Funzione sicura: formatta SOLO i numeri reali, lascia stare i testi
def format_numbers_only(val, col_name="", sheet_name=""):
  if pd.isnull(val) or val == "None":
    return val

  # Controlliamo se è un numero (int o float) o se può essere convertito in modo sicuro
  try:
    num_val = float(val)

    # Identifica se la colonna deve essere in percentuale
    is_percentage = False
    if any(
        p in str(col_name).upper() for p in ["%", "ROS", "MARGIN", "TASSO", "PESO"]
    ):
      is_percentage = True
    if sheet_name == "INPUT" and col_name == "Valore":
      is_percentage = True

    if is_percentage:
      val_pct = num_val * 100 if num_val < 1 else num_val
      return (
          f"{val_pct:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
          + "%"
      )
    else:
      return (
          f"{num_val:,.2f}"
          .replace(",", "X")
          .replace(".", ",")
          .replace("X", ".")
      )

  except (ValueError, TypeError):
    # Se il valore è un testo (stringa), lo restituisce esattamente com'è senza toccarlo
    return val


# Applichiamo la formattazione solo sulle colonne o celle che contengono dati numerici
for col in df_to_show.columns:
  df_to_show[col] = df_to_show[col].apply(
      lambda x: format_numbers_only(x, col_name=col, sheet_name=selected_sheet)
  )

st.dataframe(df_to_show, use_container_width=True)
