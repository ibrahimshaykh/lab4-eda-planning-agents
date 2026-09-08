"""
viz_utils.py
------------
Chart builders for the EDA app. Uses Plotly Express so charts are
interactive (zoom / hover / pan) instead of static matplotlib images.
"""

import pandas as pd
import plotly.express as px


CHART_TEMPLATE = "plotly_white"


def numeric_histogram(df: pd.DataFrame, column: str):
    """Interactive histogram for a numerical attribute."""
    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        color_discrete_sequence=["#4C78A8"],
        template=CHART_TEMPLATE,
        marginal="box",
    )
    fig.update_layout(
        title=f"Distribution of '{column}'",
        xaxis_title=column,
        yaxis_title="Frequency",
        bargap=0.03,
    )
    return fig


def categorical_bar_chart(df: pd.DataFrame, column: str, show_percent: bool = True):
    """Interactive bar chart of value counts for a categorical attribute."""
    counts = df[column].value_counts(dropna=False).reset_index()
    counts.columns = [column, "count"]
    counts["percent"] = (counts["count"] / counts["count"].sum() * 100).round(2)

    fig = px.bar(
        counts,
        x=column,
        y="count",
        text="percent" if show_percent else None,
        color_discrete_sequence=["#E4572E"],
        template=CHART_TEMPLATE,
    )
    if show_percent:
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(
        title=f"Frequency of Categories in '{column}'",
        xaxis_title=column,
        yaxis_title="Count",
    )
    return fig
