# Week 4 — GUI & Problem-Solving Agent

## Task 1 — Streamlit EDA Explorer
Interactive Streamlit app for CSV ingestion, metadata inspection, and attribute-level
visualization (numeric histogram / categorical bar chart), tested against `Titanic-Dataset.csv`.

- `app.py` — Streamlit UI (sidebar controls + tabbed main area)
- `data_utils.py` — dataset loading, validation, and metadata helpers
- `viz_utils.py` — Plotly chart builders
- `EDA_Notebook.ipynb` — prototype notebook backing the app

Run locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Task 2 — Cloud Resource Deployment Planning Agent
Problem-solving agent that plans the deployment of an AI application onto cloud
infrastructure (resource allocation → VM provisioning → dependency install → model
deployment → verification), minimizing total deployment time.

- `task2_cloud_deployment.py`

```bash
python task2_cloud_deployment.py
```

## Task 3 — University Course Registration Planning Agent
Problem-solving agent that guides a student through the mandatory registration workflow
(authentication → prerequisite verification → course selection → fee verification →
enrollment), minimizing registration steps.

- `task3_course_registration.py`

```bash
python task3_course_registration.py
```

Both Task 2 and Task 3 are built on a shared, reusable planning framework:

- `search_agent.py` — generic `PlanningProblem` (states, actions, transition model, goal
  test, path cost) solved with Uniform-Cost Search, so completed steps are never revisited
  and the agent always returns the minimum-cost plan, including when the state space branches.
- `Planning_Agents_Notebook.ipynb` — executed notebook demonstrating both.

## Screenshots
See `screenshots/` for the deployed EDA interface with a numerical and a categorical
attribute plotted.
