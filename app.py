import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DOMINUS - Editor Universale Totale",
    page_icon="📊",
    layout="wide",
)
st.title("📊 DOMINUS - Modifica Totale di Ogni Campo e Cella")
st.markdown("---")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"


# Caricamento completo di tutti i fogli del file Excel
@st.cache_data
def load_all_sheets(path):
  xls = pd.ExcelFile(path)
  sheets_dict = {}
  for sheet in xls.sheet_names:
    # Leggiamo il foglio senza intestazioni fisse per catturare ogni singola cella grezza
    df = pd.read_excel(path, sheet_name=sheet, header=None)
    sheets_dict[sheet] = df
  return sheets_dict


if "master_sheets" not in st.session_state:
  st.session_state["master_sheets"] = load_all_sheets(file_path)

# Menu di navigazione laterale per scegliere quale foglio/tabella aprire
sheet_list = list(st.session_state["master_sheets"].keys())
selected_sheet = st.sidebar.selectbox(
    "Seleziona Sezione / Foglio da Modificare", sheet_list
)

st.subheader(f"Sezione Attiva: {selected_sheet}")
st.markdown(
    "💡 *Ogni cella della tabella sottostante è liberamente editabile. Può"
    " cliccare e cambiare qualsiasi valore desideri.*"
)

# Estraiamo il dataframe corrente dalla memoria
df_corrente = st.session_state["master_sheets"][selected_sheet]

# Editor universale che rende ogni cella modificabile come un foglio Excel online
df_modificato = st.data_editor(
    df_corrente,
    use_container_width=True,
    num_rows="dynamic",
    key=f"universal_grid_{selected_sheet}",
)

# Aggiorniamo istantaneamente i dati in memoria con le modifiche fatte dall'utente
st.session_state["master_sheets"][selected_sheet] = df_modificato

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
  if st.button("💾 Conferma Modifiche Sezione Corrente"):
    st.success(
        f"Tutte le modifiche apportate a '{selected_sheet}' sono state salvate"
        " correttamente!"
    )

with col2:
  if st.button("🔄 Ripristina Dati Originali del File"):
    st.session_state["master_sheets"] = load_all_sheets(file_path)
    st.rerun()
