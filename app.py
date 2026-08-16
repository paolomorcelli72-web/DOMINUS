import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DOMINUS - Cabina di Regia e Modifica Totale",
    page_icon="📊",
    layout="wide",
)
st.title("📊 DOMINUS - Cabina di Regia e Modifica Live")
st.markdown("---")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"


# Caricamento dati con gestione dello stato di sessione (per mantenere le modifiche)
@st.cache_data
def load_excel_data(path):
  xls = pd.ExcelFile(path)
  sheets_data = {}
  for sheet in xls.sheet_names:
    header_row = 1 if sheet == "INPUT" else 0
    df = pd.read_excel(path, sheet_name=sheet, header=header_row)
    sheets_data[sheet] = df
  return sheets_data


if "sheets_data" not in st.session_state:
  st.session_state["sheets_data"] = load_excel_data(file_path)

sheet_names = list(st.session_state["sheets_data"].keys())

# Menu laterale di navigazione tra i fogli del file
selected_sheet = st.sidebar.selectbox("Seleziona Sezione da Modificare", sheet_names)

st.subheader(f"Area Attiva: {selected_sheet}")
st.markdown(
    "💡 *Può cliccare su qualsiasi cella della tabella (ad esempio per"
    " cambiare Milano con Bergamo nei testi) e modificarla liberamente.*"
)

# Recupera il dataframe corrente dalla sessione
df_corrente = st.session_state["sheets_data"][selected_sheet]

# Editor universale interattivo abilitato alla scrittura su ogni cella
df_modificato = st.data_editor(
    df_corrente,
    use_container_width=True,
    num_rows="dynamic",
    key=f"editor_live_{selected_sheet}",
)

# Aggiorna i dati nella sessione quando l'utente modifica la tabella
st.session_state["sheets_data"][selected_sheet] = df_modificato

# Pulsante per confermare e applicare i calcoli
col1, col2 = st.columns([2, 8])
with col1:
  if st.button("💾 Salva e Aggiorna Motore"):
    st.success(f"Dati della sezione '{selected_sheet}' aggiornati con successo!")

with col2:
  if st.button("🔄 Ripristina Dati Originali"):
    st.session_state["sheets_data"] = load_excel_data(file_path)
    st.rerun()

# Sezione di riscontro rapido per i fogli di intervista (es. Assetto, Patrimonio, ecc.)
if selected_sheet in ["ASSETTO", "PATRIMONIO", "VALORE", "CUSTODIA", "LEADER"]:
  st.markdown("---")
  st.subheader("📊 Simulazione Punteggio Area")
  score_totale = 0
  df_attivo = st.session_state["sheets_data"][selected_sheet]

  if "Valore" in df_attivo.columns and "Risposta" in df_attivo.columns:
    for idx, row in df_attivo.iterrows():
      resp = str(row.get("Risposta", "")).strip().upper()
      val = row.get("Valore", 0)
      if resp == "NO" and pd.notnull(val):
        try:
          score_totale += float(val)
        except:
          pass

  st.metric(
      label="Vulnerabilità Calcolata per questa Area",
      value=f"{score_totale:.2f} punti",
  )
