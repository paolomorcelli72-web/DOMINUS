import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DOMINUS - Cabina di Regia e Scoring",
    page_icon="📊",
    layout="wide",
)
st.title("📊 DOMINUS - Cabina di Regia e Scoring Dinamico")
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

# Menu di navigazione laterale
menu = st.sidebar.selectbox(
    "Seleziona Sezione",
    [
        "Quadro di Controllo",
        "Intervista & Scoring Live",
        "Dati Ufficiali (INPUT)",
        "Anagrafica",
        "Assetto",
        "Patrimonio",
        "Valore",
        "Custodia",
        "Leader",
        "Dominus Score",
    ],
)


# Funzione di formattazione numeri interi / percentuali
def format_val(val, is_pct=False):
  if pd.isnull(val) or val == "None":
    return val
  try:
    num = float(val)
    if is_pct:
      return f"{round(num * 100):,}%".replace(",", ".")
    return f"{round(num):,}".replace(",", ".")
  except (ValueError, TypeError):
    return val


if menu == "Quadro di Controllo":
  st.subheader("Quadro di Controllo Aziendale")
  df_qc = sheets_data["QUADRO DI CONTROLLO "].copy()
  st.dataframe(df_qc, use_container_width=True)

elif menu == "Dati Ufficiali (INPUT)":
  st.subheader("Base Dati Ufficiali e Pesi")
  st.dataframe(sheets_data["INPUT"], use_container_width=True)

elif menu == "Dominus Score":
  st.subheader("Risultati Sintetici e Rating DSI")
  st.dataframe(sheets_data["DOMINUS SCORE"], use_container_width=True)

elif menu in ["Assetto", "Patrimonio", "Valore", "Custodia", "Leader"]:
  st.subheader(f"Area: {menu}")
  df_area = sheets_data[menu.upper()].copy()
  st.markdown(
    "Qui può consultare le domande e i pesi associati estratti dal modello."
  )
  st.dataframe(df_area, use_container_width=True)

elif menu == "Intervista & Scoring Live":
  st.subheader("🎙️ Motore di Intervista e Calcolo Scoring in Tempo Reale")
  st.markdown(
    "Modifichi le risposte o i parametri chiave per vedere il ricalcolo"
    " immediato del Dominus Score."
  )

  # Esempio di simulazione interattiva basata sull'area Assetto
  df_assetto = sheets_data["ASSETTO"].copy()

  st.markdown("### Sezione Simulazione Assetti Critici")
  edited_assetto = st.data_editor(df_assetto, use_container_width=True)

  if st.button("Ricalcola Dominus Score Dinamico"):
    # Motore di calcolo basato sulle risposte SI/NO modificate nell'editor
    # Se la risposta è 'NO', somma il valore di rischio associato
    score_totale = 0
    if "Risposta" in edited_assetto.columns and "Valore" in edited_assetto.columns:
      for idx, row in edited_assetto.iterrows():
        if str(row["Risposta"]).strip().upper() == "NO":
          score_totale += float(row["Valore"] if pd.notnull(row["Valore"]) else 0)

    st.success("Calcolo completato con successo!")
    st.metric(
        label="DOMINUS SCORE DINAMICO SIMULATO",
        value=f"{score_totale:.2f} punti",
    )

    if score_totale < 45:
      st.info(
          "✅ **Esito**: Profilo rientrante nei Range di Sicurezza (< 45)."
          " Azienda Bancabile."
      )
    else:
      st.warning(
          "⚠️ **Esito**: Superamento della soglia di guardia. Attivare il"
          " Recovery Plan."
      )
