import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DOMINUS - Gestione Totale Sezioni", page_icon="📊", layout="wide"
)
st.title("📊 DOMINUS - Modifica e Gestione di Tutte le Tabelle")
st.markdown("---")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"


@st.cache_data
def load_all_data(path):
  xls = pd.ExcelFile(path)
  sheets = {}
  for s in xls.sheet_names:
    sheets[s] = pd.read_excel(path, sheet_name=s, header=None)
  return sheets


if "master_data" not in st.session_state:
  st.session_state["master_data"] = load_all_data(file_path)

# Menu di selezione di tutti i fogli del file
sheet_list = list(st.session_state["master_data"].keys())
selected_sheet = st.sidebar.selectbox(
    "Seleziona Sezione da Modificare", sheet_list
)

st.subheader(f"Sezione Attiva: {selected_sheet}")
df_corrente = st.session_state["master_data"][selected_sheet]

st.markdown(
    "💡 *Modifichi i valori direttamente nei campi sottostanti. Ogni casella"
    " corrisponde a una cella della tabella originale.*"
)

# Creazione dinamica di un modulo di input per ogni riga e cella della tabella attiva
with st.form(f"form_univoco_{selected_sheet}"):
  righe, colonne = df_corrente.shape
  nuovi_dati = []

  # Mostriamo le righe in modo ordinato con campi di testo modificabili
  for r in range(righe):
    st.markdown(f"**Riga {r+1}**")
    cols = st.columns(min(colonne, 4))  # Suddivide in colonne per leggibilità
    riga_valori = []
    for c in range(colonne):
      valore_cella = df_corrente.iloc[r, c]
      valore_str = "" if pd.isnull(valore_cella) else str(valore_cella)

      with cols[c % len(cols)]:
        # Campo di input testuale per ogni singola cella
        val_mod = st.text_input(
            f"R{r+1}C{c+1}", value=valore_str, key=f"cell_{selected_sheet}_{r}_{c}"
        )
        riga_valori.append(val_mod)
    nuovi_dati.append(riga_valori)
    st.markdown("---")

  salva_tutto = st.form_submit_button(
      f"💾 Salva Modifiche per {selected_sheet}"
  )

  if salva_tutto:
    # Aggiorniamo il dataframe in memoria con i nuovi valori inseriti
    nuovo_df = pd.DataFrame(nuovi_dati)
    st.session_state["master_data"][selected_sheet] = nuovo_df
    st.success(
        f"✅ Tutti i dati della sezione '{selected_sheet}' sono stati aggiornati"
        " con successo!"
    )

# Sezione di riscontro visivo della tabella aggiornata
st.subheader("Visualizzazione Tabella Attuale")
st.dataframe(
    st.session_state["master_data"][selected_sheet], use_container_width=True
)
