"""
data_utils.py
--------------
Helper functions for loading a CSV dataset and extracting metadata
(shape, dtypes, missing values, summary statistics) for the EDA app.
Kept separate from app.py so the Streamlit UI code stays thin.
"""

import pandas as pd


class InvalidCSVError(Exception):
    """Raised when the uploaded file cannot be parsed as a proper CSV."""
    pass


def load_dataset(uploaded_file) -> pd.DataFrame:
    """
    Read an uploaded file-like object into a pandas DataFrame.
    Raises InvalidCSVError with a friendly message on failure.
    """
    if uploaded_file is None:
        raise InvalidCSVError("No file was provided.")

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as exc:
        raise InvalidCSVError(f"The file could not be parsed as CSV ({exc}).") from exc

    if df.empty or df.shape[1] == 0:
        raise InvalidCSVError("The uploaded CSV appears to be empty.")

    return df


def dataset_shape(df: pd.DataFrame) -> tuple:
    """Return (n_rows, n_cols)."""
    return df.shape[0], df.shape[1]


def dtype_table(df: pd.DataFrame) -> pd.DataFrame:
    """One row per column: name + inferred pandas dtype."""
    return (
        df.dtypes
        .astype(str)
        .reset_index()
        .rename(columns={"index": "Column", 0: "Dtype"})
    )


def missing_value_table(df: pd.DataFrame) -> pd.DataFrame:
    """Per-column count and percentage of missing values."""
    counts = df.isna().sum()
    pct = (counts / len(df) * 100).round(2)
    out = pd.DataFrame({
        "Column": counts.index,
        "Missing Values": counts.values,
        "Missing (%)": pct.values,
    })
    return out.sort_values("Missing Values", ascending=False).reset_index(drop=True)


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """mean / median / min / max (+ std, quartiles) for numeric columns only."""
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] == 0:
        return pd.DataFrame()
    summary = numeric_df.describe().T
    summary["median"] = numeric_df.median()
    ordered_cols = ["mean", "median", "min", "max", "std", "25%", "50%", "75%"]
    ordered_cols = [c for c in ordered_cols if c in summary.columns]
    return summary[ordered_cols].round(3)


def classify_column(df: pd.DataFrame, column: str) -> str:
    """Return 'numerical' or 'categorical' for the given column."""
    return "numerical" if pd.api.types.is_numeric_dtype(df[column]) else "categorical"
