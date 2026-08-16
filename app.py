import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles.numbers import is_date_format

FILE_XLSX = "DOMINUS 2026 DEFINITIVO.xlsx"

st.set_page_config(
    page_title="DOMINUS 2026",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DOMINUS 2026 - Editor Online")


def format_excel_value(cell):

    value = cell.value

    if value is None:
        return ""

    fmt = str(cell.number_format)

    try:

        # Percentuali
        if "%" in fmt and isinstance(value, (int, float)):
            perc = value * 100

            if ".00" in fmt or "0.00%" in fmt:
                return f"{perc:.2f}%".replace(".", ",")

            return f"{perc:.0f}%"

        # Date
        if is_date_format(fmt):
            return value.strftime("%d/%m/%Y")

        # Numeri
        if isinstance(value, (int, float)):

            if abs(value) >= 1000:

                txt = f"{value:,.2f}"

                txt = (
                    txt.replace(",", "§")
                       .replace(".", ",")
                       .replace("§", ".")
                )

                if txt.endswith(",00"):
                    txt = txt[:-3]

                return txt

            else:

                txt = str(value)

                if "." in txt:
                    txt = txt.replace(".", ",")

                return txt

        return str(value)

    except:
        return str(value)


@st.cache_resource
def load_workbook_cached():
    return load_workbook(
        FILE_XLSX,
        data_only=False
    )


wb = load_workbook_cached()

sheet_name = st.sidebar.selectbox(
    "Seleziona Foglio",
    wb.sheetnames
)

ws = wb[sheet_name]

rows = []

max_col = ws.max_column

for row in ws.iter_rows():

    values = []

    for cell in row:
        values.append(format_excel_value(cell))

    while len(values) < max_col:
        values.append("")

    rows.append(values)

if len(rows) == 0:
    df = pd.DataFrame()
else:
    df = pd.DataFrame(rows)

column_config = {
    col: st.column_config.TextColumn(
        str(col),
        width="medium"
    )
    for col in df.columns
}

st.subheader(sheet_name)

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    column_config=column_config,
    key=f"editor_{sheet_name}"
)

if st.button("💾 Salva Workbook", type="primary"):

    wb_save = load_workbook(
        FILE_XLSX,
        data_only=False
    )

    ws_save = wb_save[sheet_name]

    for r in range(len(edited_df)):

        for c in range(len(edited_df.columns)):

            value = edited_df.iat[r, c]

            if value == "":
                value = None

            ws_save.cell(
                row=r + 1,
                column=c + 1
            ).value = value

    wb_save.save(FILE_XLSX)

    st.success("✅ Modifiche salvate correttamente.")

    st.cache_resource.clear()

    st.rerun()
