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


# Caricamento completo di tutti i fogli del file Excel originale
@st.cache_data
def load_all_sheets(path):
  xls = pd.ExcelFile(path)
  sheets_dict = {}
  for sheet in xls.sheet_names:
    df = pd.read_excel(path, sheet_name=sheet, header=None)
    # Convertiamo tutte le colonne in stringhe per evitare conflitti di tipo durante l'editing
    df = df.astype(str)
    df = df.replace("nan", "")
    sheets_dict[sheet] = df
  return sheets_dict


if "master_sheets" not in st.session_state:
  st.session_state["master_sheets"] = load_all_sheets(file_path)

# Menu laterale per scegliere quale foglio/tabella modificare
sheet_list = list(st.session_state["master_sheets"].keys())
selected_sheet = st.sidebar.selectbox("Seleziona Sezione da Modificare", sheet_list)

st.subheader(f"Sezione Attiva: {selected_sheet}")
st.markdown(
    "💡 *Ogni cella della tabella sottostante è interamente editabile. Può"
    " cliccare su qualsiasi casella, cancellare e scrivere il valore che"
    " desidera (es. da MILANO a BERGAMO).* "
)

# Estraiamo il dataframe corrente dalla memoria di sessione
df_corrente = st.session_state["master_sheets"][selected_sheet]

# Editor interattivo totale per ogni cella della griglia
df_modificato = st.data_editor(
    df_corrente,
    use_container_width=True,
    num_rows="dynamic",
    key=f"grid_totale_{selected_sheet}",
)

# Salvataggio istantaneo delle modifiche nella sessione
st.session_state["master_sheets"][selected_sheet] = df_modificato

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
  if st.button("💾 Conferma e Salva Modifiche Sezione"):
    st.success(
        f"Tutte le modifiche apportate alla sezione '{selected_sheet}' sono"
        " state salvate con successo!"
    )

with col2:
  if st.button("🔄 Ripristina Dati Originali"):
    st.session_state["master_sheets"] = load_all_sheets(file_path)
    st.rerun()
