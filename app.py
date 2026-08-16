import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DOMINUS - Gestione e Modifica Dati",
    page_icon="📊",
    layout="wide",
)
st.title("📊 DOMINUS - Modifica Dati Aziendali")
st.markdown("---")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"


@st.cache_data
def load_data(path):
  xls = pd.ExcelFile(path)
  sheets = {}
  for s in xls.sheet_names:
    sheets[s] = pd.read_excel(path, sheet_name=s, header=None)
  return sheets


if "master_data" not in st.session_state:
  st.session_state["master_data"] = load_data(file_path)

# Selezioniamo il foglio
sheet_list = list(st.session_state["master_data"].keys())
selected_sheet = st.sidebar.selectbox("Seleziona Sezione", sheet_list)

st.subheader(f"Sezione: {selected_sheet}")
df_corrente = st.session_state["master_data"][selected_sheet]

# Se siamo in ANAGRAFICA, creiamo un modulo interattivo super comodo per iPad
if selected_sheet == "ANAGRAFICA":
  st.markdown(
      "💡 *Modifichi direttamente i campi sottostanti per aggiornare i dati"
      " aziendali (es. da MILANO a BERGAMO).* "
  )

  # Estraiamo i valori attuali dalle celle note del file Excel
  ragione_soc = str(df_corrente.iloc[0, 1])
  cf = str(df_corrente.iloc[0, 3])
  piva = str(df_corrente.iloc[1, 1])
  forma_giur = str(df_corrente.iloc[1, 3])
  sede_op = str(df_corrente.iloc[3, 1])
  data_cost = str(df_corrente.iloc[3, 3])
  dip = str(df_corrente.iloc[4, 1])
  sede_leg = str(df_corrente.iloc[4, 3])
  fatt = str(df_corrente.iloc[5, 1])

  with st.form("form_anagrafica_mod"):
    col1, col2 = st.columns(2)
    with col1:
      r_soc = st.text_input("Ragione Sociale", value=ragione_soc)
      c_fisc = st.text_input("Codice Fiscale", value=cf)
      p_iva = st.text_input("Partita IVA", value=piva)
      f_giur = st.text_input("Forma Giuridica", value=forma_giur)
      s_op = st.text_input("Sede Operativa", value=sede_op)
    with col2:
      d_cost = st.text_input("Data Costituzione", value=data_cost)
      n_dip = st.text_input("Dipendenti", value=dip)
      s_leg = st.text_input("Sede Legale (es. Bergamo)", value=sede_leg)
      f_att = st.text_input("Fatturato", value=fatt)

    salva_btn = st.form_submit_button("💾 Salva Modifiche Anagrafica")

    if salva_btn:
      df_corrente.iloc[0, 1] = r_soc
      df_corrente.iloc[0, 3] = c_fisc
      df_corrente.iloc[1, 1] = p_iva
      df_corrente.iloc[1, 3] = f_giur
      df_corrente.iloc[3, 1] = s_op
      df_corrente.iloc[3, 3] = d_cost
      df_corrente.iloc[4, 1] = n_dip
      df_corrente.iloc[4, 3] = s_leg
      df_corrente.iloc[5, 1] = f_att

      st.session_state["master_data"]["ANAGRAFICA"] = df_corrente
      st.success("✅ Dati anagrafici aggiornati con successo!")

  st.markdown("---")
  st.subheader("Visualizzazione Tabella Aggiornata")
  st.dataframe(df_corrente, use_container_width=True)

else:
  # Per gli altri fogli mostriamo la tabella con avviso
  st.markdown(
      "Visualizzazione dati della sezione. Per modificare parametri specifici"
      " selezioni la casella o utilizzi i moduli dedicati."
  )
  edited_df = st.data_editor(
      df_corrente, use_container_width=True, key=f"edit_{selected_sheet}"
  )
  st.session_state["master_data"][selected_sheet] = edited_df
