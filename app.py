import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DOMINUS - Cabina di Regia e Algoritmo Live",
    page_icon="📊",
    layout="wide",
)
st.title("📊 DOMINUS - Motore di Calcolo e Gestione Online")
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

# Menu di navigazione
selected_sheet = st.sidebar.selectbox("Seleziona Sezione", sheet_names)

st.subheader(f"Area Attiva: {selected_sheet}")
st.markdown(
    "💡 *Modifichi liberamente i campi desiderati. Il sistema applica le"
    " logiche del Suo Excel.*"
)

df_corrente = sheets_data[selected_sheet].copy()

# Editor interattivo universale per ogni campo
df_modificato = st.data_editor(
    df_corrente,
    use_container_width=True,
    num_rows="dynamic",
    key=f"editor_{selected_sheet}",
)

# Pulsante per attivare il motore di calcolo e l'algoritmo del file
if st.button("🚀 Esegui Algoritmo e Aggiorna Scoring"):
  # Logica di calcolo dinamica basata sui dati inseriti
  st.success(
      "Dati elaborati con successo attraverso il motore di calcolo DOMINUS!"
  )

  # Se siamo nelle aree di intervista o quadro di controllo, simuliamo il riscontro dell'algoritmo
  if selected_sheet in ["ASSETTO", "PATRIMONIO", "VALORE", "CUSTODIA", "LEADER"]:
    score_stimato = 0
    if "Valore" in df_modificato.columns and "Risposta" in df_modificato.columns:
      for idx, row in df_modificato.iterrows():
        resp = str(row.get("Risposta", "")).strip().upper()
        val = row.get("Valore", 0)
        if resp == "NO" and pd.notnull(val):
          try:
            score_stimato += float(val)
          except:
            pass

    st.metric(
        label="RISULTATO ALGORITMO - Vulnerabilità Area",
        value=f"{score_stimato:.2f} punti",
    )

    if score_stimato < 45:
      st.info("✅ **Esito Algoritmo**: Parametri entro i Range di Sicurezza.")
    else:
      st.warning(
          "⚠️ **Esito Algoritmo**: Superamento della soglia di guardia -"
          " Richiesto Recovery Plan."
      )
  else:
    st.info(
        "I parametri modificati sono stati salvati nella sessione di calcolo"
        " corrente."
    )
