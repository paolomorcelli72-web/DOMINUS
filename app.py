import streamlit as st

st.set_page_config(page_title="DOMINUS - Intervista", layout="centered")

st.title("📊 Intervista DOMINUS")
st.markdown("Risponda alle seguenti domande per calcolare il Suo Score.")

# Creiamo una sessione per salvare le risposte
if 'risposte' not in st.session_state:
    st.session_state.risposte = {}

# Esempio di Intervista (può aggiungere tutte le domande che vuole)
tab1, tab2 = st.tabs(["Fase 1: Dati Aziendali", "Fase 2: Analisi Rischi"])

with tab1:
    st.session_state.risposte['fatturato'] = st.number_input("Inserisca il fatturato previsto:", min_value=0)
    st.session_state.risposte['dipendenti'] = st.slider("Numero di dipendenti:", 0, 500, 10)

with tab2:
    st.session_state.risposte['rischio_mercato'] = st.radio("Come valuta il rischio mercato?", ["Basso", "Medio", "Alto"])

# Bottone di calcolo finale
if st.button("CALCOLA DOMINUS SCORE"):
    # Qui inseriremo la logica di calcolo basata sul Suo file Excel
    st.success("Analisi completata!")
    st.write("Le Sue risposte:", st.session_state.risposte)
    st.metric(label="DOMINUS SCORE FINALE", value="78/100")
