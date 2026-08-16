import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DOMINUS - Editor Speciale INPUT",
    page_icon="📊",
    layout="wide",
)
st.title("📊 DOMINUS - Modifica Totale (Focus Sezione INPUT)")
st.markdown("---")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(file_path, sheet_name=None, header=None)

if "master_data" not in st.session_state:
    st.session_state["master_data"] = load_data()

# Selezione Sezione
sheet_names = list(st.session_state["master_data"].keys())
selected_sheet = st.sidebar.selectbox("Seleziona Sezione", sheet_names, index=sheet_names.index("INPUT"))

st.subheader(f"Area Attiva: {selected_sheet}")

# Editor Speciale che preserva i formati
df_corrente = st.session_state["master_data"][selected_sheet]

# Sezione specifica per il foglio INPUT: vogliamo che ogni cella sia editabile
# Utilizziamo un editor che non forzi la conversione in stringa, mantenendo intatte le %
df_modificato = st.data_editor(
    df_corrente,
    use_container_width=True,
    num_rows="dynamic",
    key=f"editor_{selected_sheet}"
)

# Salvataggio
if st.button("💾 Salva Modifiche per questa Sezione"):
    st.session_state["master_data"][selected_sheet] = df_modificato
    st.success(f"Modifiche salvate con successo nel foglio {selected_sheet}!")

# Mostriamo i dati correnti per controllo
st.markdown("---")
st.write("Visualizzazione Dati Correnti:")
st.dataframe(st.session_state["master_data"][selected_sheet], use_container_width=True)
