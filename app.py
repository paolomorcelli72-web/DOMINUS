import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DOMINUS - Cabina di Regia e Modifica Totale",
    page_icon="📊",
    layout="wide",
)
st.title("📊 DOMINUS - Cabina di Regia e Gestione Online")
st.markdown("---")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"


# Caricamento pulito e standard dei fogli dal file Excel originale
@st.cache_data
def load_excel_standard(path):
  xls = pd.ExcelFile(path)
  sheets_dict = {}
  for sheet in xls.sheet_names:
    header_row = 1 if sheet == "INPUT" else 0
    df = pd.read_excel(path, sheet_name=sheet, header=header_row)
    sheets_dict[sheet] = df
  return sheets_dict


# Inizializziamo lo stato della sessione per mantenere le modifiche fatte online
if "user_sheets" not in st.session_state:
  st.session_state["user_sheets"] = load_excel_standard(file_path)

# Menu laterale di selezione foglio
sheet_names_list = list(st.session_state["user_sheets"].keys())
selected_sheet = st.sidebar.selectbox("Seleziona Sezione del File", sheet_names_list)

st.subheader(f"Sezione Attiva: {selected_sheet}")
st.markdown(
    "💡 *Il file di partenza è quello originale. Ora può cliccare su qualsiasi"
    " cella della tabella sottostante, modificare qualsiasi testo o numero (es."
    " cambiare i dati anagrafici) e il sistema salverà tutto in tempo reale.*"
)

# Recuperiamo il DataFrame corrente dalla sessione
df_corrente = st.session_state["user_sheets"][selected_sheet]

# Editor interattivo abilitato per la modifica totale di ogni cella
df_modificato = st.data_editor(
    df_corrente,
    use_container_width=True,
    num_rows="dynamic",
    key=f"editor_tab_{selected_sheet}",
)

# Salvataggio automatico delle modifiche nello stato della sessione
st.session_state["user_sheets"][selected_sheet] = df_modificato

st.markdown("---")
col1, col2 = st.columns([1, 1])

with col1:
  if st.button("💾 Conferma e Salva Modifiche"):
    st.success(
        f"Le modifiche alla sezione '{selected_sheet}' sono state registrate"
        " correttamente!"
    )

with col2:
  if st.button("🔄 Ripristina Dati Originali"):
    st.session_state["user_sheets"] = load_excel_standard(file_path)
    st.rerun()
