import streamlit as st
import pandas as pd

st.set_page_config(page_title="DOMINUS", layout="wide")
st.title("📊 DOMINUS - Cabina di Regia")

file_path = "DOMINUS 2026 DEFINITIVO.xlsx"

@st.cache_data
def load_data():
    return pd.ExcelFile(file_path)

try:
    xls = load_data()
    sheet = st.sidebar.selectbox("Seleziona Area", xls.sheet_names)
    st.subheader(f"Area: {sheet}")
    st.dataframe(pd.read_excel(file_path, sheet_name=sheet), use_container_width=True)
except Exception as e:
    st.error(f"Errore: {e}")
