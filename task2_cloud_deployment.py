"""
Task 2 — Cloud Resource Deployment Planning Agent
---------------------------------------------------
A problem-solving agent that plans the deployment of an AI application
onto cloud infrastructure: resource allocation, VM provisioning,
dependency installation, model deployment, and service verification.

Goal Formulation
    Goal state: AI application deployed successfully.
    Performance measure: minimize deployment time (and cost, modeled
    here as time since each cloud operation is billed by duration).

Problem Formulation
    Initial state : S0  "Deployment Request Received"
    Goal state    : S6  "Deployment Completed"
    Actions       : Allocate Resources, Create VM, Use Prebuilt VM Image,
                    Install Dependencies, Deploy AI Model, Verify Deployment,
                    Confirm Completion.
    Transition model : each action moves the deployment to the next state.
    Goal test     : state == "Deployment Completed".
    Path cost     : sum of each action's execution time (minutes).

Two provisioning routes are modeled after "Resources Allocated" —
a full VM build vs. a prebuilt image — so the planner has an actual
choice to make rather than a single forced sequence, and Uniform-Cost
Search is what picks the cheaper route.
"""

from search_agent import PlanningProblem, uniform_cost_search, describe_state_space, describe_solution


def build_problem() -> PlanningProblem:
    problem = PlanningProblem(initial_state="S0: Request Received", goal_state="S6: Deployment Completed")

    problem.add_transition("S0: Request Received", "Allocate Resources", "S1: Resources Allocated", 2)

    # Two alternative routes from "Resources Allocated" to "Dependencies Installed"
    problem.add_transition("S1: Resources Allocated", "Create Virtual Machine", "S2a: VM Created", 4)
    problem.add_transition("S2a: VM Created", "Install Dependencies", "S3: Dependencies Installed", 3)

    problem.add_transition("S1: Resources Allocated", "Use Prebuilt VM Image", "S2b: Prebuilt VM Ready", 3)
    problem.add_transition("S2b: Prebuilt VM Ready", "Install Dependencies", "S3: Dependencies Installed", 5)

    problem.add_transition("S3: Dependencies Installed", "Deploy AI Model", "S4: Model Deployed", 5)
    problem.add_transition("S4: Model Deployed", "Verify Deployment", "S5: Deployment Verified", 2)
    problem.add_transition("S5: Deployment Verified", "Confirm Completion", "S6: Deployment Completed", 1)

    return problem


def run():
    problem = build_problem()
    print(describe_state_space(problem))
    print()

    result = uniform_cost_search(problem)
    print(describe_solution(result, unit="min"))


if __name__ == "__main__":
    run()
