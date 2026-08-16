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


# Funzione per mostrare solo numeri interi con separatore delle migliaia
def format_integers_only(val, col_name="", sheet_name="", row_label=""):
  if pd.isnull(val) or val == "None":
    return val

  str_label = str(row_label).upper()
  if "ANAGRAFICA" in sheet_name.upper() and (
      "IVA" in str_label
      or "ATECO" in str_label
      or "CODICE" in str_label
      or "P.IVA" in str_label
  ):
    return str(val).replace(".0", "")

  try:
    num_val = float(val)

    is_percentage = False
    if any(
        p in str(col_name).upper() for p in ["%", "ROS", "MARGIN", "TASSO", "PESO"]
    ):
      is_percentage = True
    if sheet_name == "INPUT" and col_name == "Valore":
      is_percentage = True

    if is_percentage:
      val_pct = num_val * 100 if num_val < 1 else num_val
      # Percentuale intera o con 1 decimale se serve, qui arrotondata a intero con %
      return f"{round(val_pct):,}".replace(",", ".") + "%"
    else:
      if num_val > 1000000000 and not any(
          k in str(col_name).upper() for k in ["VALORE", "IMPORTO", "FATTURATO"]
      ):
        return str(val).replace(".0", "")
      # Mostra solo numeri interi con il punto per le migliaia (senza decimali)
      return f"{round(num_val):,}".replace(",", ".")

  except (ValueError, TypeError):
    return val


label_col = df_to_show.columns[0] if len(df_to_show.columns) > 0 else None

for col in df_to_show.columns:
  df_to_show[col] = [
      format_integers_only(
          df_to_show.loc[i, col],
          col_name=col,
          sheet_name=selected_sheet,
          row_label=df_to_show.loc[i, label_col] if label_col else "",
      )
      for i in df_to_show.index
  ]

st.dataframe(df_to_show, use_container_width=True)
