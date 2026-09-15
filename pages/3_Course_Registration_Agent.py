"""
Task 3 page — University Course Registration Planning Agent.

Renders the same problem formulation and Uniform-Cost Search solution as
`task3_course_registration.py`, so the agent can be demonstrated from the
GUI instead of the terminal. The planning logic itself is imported, not
duplicated.
"""

import streamlit as st

from task3_course_registration import build_problem
from search_agent import uniform_cost_search, describe_state_space, describe_solution

st.set_page_config(page_title="Course Registration Agent", page_icon="🎓", layout="wide")

st.title("Task 3 — University Course Registration Planning Agent")
st.caption(
    "Guides a student through the mandatory registration workflow, "
    "minimizing the number of registration steps."
)

problem = build_problem()

st.subheader("Goal Formulation")
st.markdown(
    f"""
- **Initial state:** `{problem.initial_state}`
- **Goal state:** `{problem.goal_state}`
- **Performance measure:** minimize registration steps while satisfying every
  mandatory academic requirement
"""
)

st.subheader("State Space")
st.code(describe_state_space(problem), language="text")

st.subheader("Optimal Plan (Uniform-Cost Search)")
result = uniform_cost_search(problem)
st.code(describe_solution(result, unit="step(s)"), language="text")

if result is not None:
    st.metric("Total Path Cost", f"{result['total_cost']} step(s)")
