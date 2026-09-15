"""
Task 2 page — Cloud Resource Deployment Planning Agent.

Renders the same problem formulation and Uniform-Cost Search solution as
`task2_cloud_deployment.py`, so the agent can be demonstrated from the GUI
instead of the terminal. The planning logic itself is imported, not
duplicated.
"""

import streamlit as st

from task2_cloud_deployment import build_problem
from search_agent import uniform_cost_search, describe_state_space, describe_solution

st.set_page_config(page_title="Cloud Deployment Agent", page_icon="☁️", layout="wide")

st.title("Task 2 — Cloud Resource Deployment Planning Agent")
st.caption(
    "Plans the deployment of an AI application onto cloud infrastructure, "
    "minimizing total deployment time."
)

problem = build_problem()

st.subheader("Goal Formulation")
st.markdown(
    f"""
- **Initial state:** `{problem.initial_state}`
- **Goal state:** `{problem.goal_state}`
- **Performance measure:** minimize total deployment time (minutes)
"""
)

st.subheader("State Space")
st.code(describe_state_space(problem), language="text")

st.subheader("Optimal Plan (Uniform-Cost Search)")
result = uniform_cost_search(problem)
st.code(describe_solution(result, unit="min"), language="text")

if result is not None:
    st.metric("Total Deployment Time", f"{result['total_cost']} min")
