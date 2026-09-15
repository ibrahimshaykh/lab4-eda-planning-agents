"""
Exploratory Data Analysis (EDA) Explorer
-----------------------------------------
Week 4 Lab Task 1 — Streamlit-based GUI for dataset ingestion, metadata
inspection, and attribute-level visual pattern recognition.

Run locally with:  streamlit run app.py
"""

import streamlit as st

from data_utils import (
    InvalidCSVError,
    load_dataset,
    dataset_shape,
    dtype_table,
    missing_value_table,
    numeric_summary,
    classify_column,
)
from viz_utils import numeric_histogram, categorical_bar_chart


st.set_page_config(
    page_title="EDA Explorer",
    page_icon="🔎",
    layout="wide",
)


# ----------------------------------------------------------------------
# Sidebar — all interactive controls live here
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("🔎 EDA Explorer")
    st.caption("Upload a CSV to begin exploring it.")

    uploaded_file = st.file_uploader("Upload dataset (.csv)", type=["csv"])

    st.divider()
    st.caption("Tested with the Titanic dataset (`Titanic-Dataset.csv`).")

    selected_column = None  # populated below once a dataset is loaded


# ----------------------------------------------------------------------
# Main area
# ----------------------------------------------------------------------
st.title("Exploratory Data Analysis Explorer")

if uploaded_file is None:
    st.info("⬅️ Upload a CSV file from the sidebar to get started.")
    st.stop()

try:
    df = load_dataset(uploaded_file)
except InvalidCSVError as err:
    st.error(f"⚠️ {err}")
    st.stop()

n_rows, n_cols = dataset_shape(df)

# Attribute selector now that we know the columns
with st.sidebar:
    selected_column = st.selectbox("Select attribute to visualize", df.columns, index=0)
    attr_type = classify_column(df, selected_column)
    st.write(f"Detected type: **{attr_type}**")


overview_tab, missing_tab, stats_tab, viz_tab = st.tabs(
    ["📄 Preview", "🧩 Missing Values", "📈 Summary Stats", "📊 Visualization"]
)

with overview_tab:
    # st.metric follows the active Streamlit theme, so these stay readable
    # in both light and dark mode.
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{n_rows:,}")
    c2.metric("Columns", f"{n_cols:,}")
    c3.metric("Total Missing Cells", f"{int(df.isna().sum().sum()):,}")

    st.subheader("First 5 Rows")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("Column Data Types")
    st.dataframe(dtype_table(df), use_container_width=True, hide_index=True)

with missing_tab:
    st.subheader("Missing Values per Attribute")
    st.dataframe(missing_value_table(df), use_container_width=True, hide_index=True)

with stats_tab:
    st.subheader("Basic Statistics — Numerical Attributes")
    summary = numeric_summary(df)
    if summary.empty:
        st.warning("No numerical columns found in this dataset.")
    else:
        st.dataframe(summary, use_container_width=True)

with viz_tab:
    st.subheader(f"Visualization for '{selected_column}' ({attr_type})")

    if attr_type == "numerical":
        fig = numeric_histogram(df, selected_column)
    else:
        show_pct = st.checkbox("Show percentage labels", value=True)
        fig = categorical_bar_chart(df, selected_column, show_percent=show_pct)

    st.plotly_chart(fig, use_container_width=True)
