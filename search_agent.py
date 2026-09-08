"""
search_agent.py
----------------
A small, reusable problem-solving agent framework used by Task 2
(Cloud Resource Deployment Planning) and Task 3 (Course Registration
Planning). Modeling the classic PEAS / problem-formulation pieces
(states, actions, transition model, goal test, path cost) as one
generic PlanningProblem, with Uniform-Cost Search as the search
strategy, keeps the two task scripts short and lets the same,
independently-testable planner back both of them.
"""

import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(order=True)
class Transition:
    """A single directed edge in the state space: performing `action`
    while in the source state moves the agent to `target` at `cost`."""
    action: str = field(compare=False)
    target: str = field(compare=False)
    cost: float = field(compare=False)


class PlanningProblem:
    """
    Generic problem formulation:
      - states are plain strings (state identifiers)
      - actions/transition-model are edges attached to a source state
      - goal test compares against a single goal state
      - path cost accumulates edge weights
    """

    def __init__(self, initial_state: str, goal_state: str):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self._graph: Dict[str, List[Transition]] = {initial_state: [], goal_state: []}

    def add_transition(self, source: str, action: str, target: str, cost: float) -> None:
        self._graph.setdefault(source, []).append(Transition(action, target, cost))
        self._graph.setdefault(target, [])

    def possible_actions(self, state: str) -> List[Transition]:
        return self._graph.get(state, [])

    def goal_test(self, state: str) -> bool:
        return state == self.goal_state

    def state_space(self) -> Dict[str, List[Tuple[str, str, float]]]:
        """Full adjacency-list view of every reachable transition — the
        'complete deployment/registration state space' the lab asks for."""
        return {
            state: [(t.action, t.target, t.cost) for t in edges]
            for state, edges in self._graph.items()
        }

    def states(self) -> List[str]:
        return list(self._graph.keys())


def uniform_cost_search(problem: PlanningProblem):
    """
    Expands the cheapest frontier node first (a priority queue keyed on
    accumulated path cost) and never re-expands a state already visited,
    so completed steps are never revisited and the search terminates on
    any graph, including one with alternative/branching paths.

    Returns a dict with the optimal state sequence, the action sequence
    (name + individual cost), and the total path cost — or None if the
    goal is unreachable.
    """
    counter = 0  # tie-breaker so the heap never compares path lists
    frontier = [(0.0, counter, problem.initial_state, [problem.initial_state], [])]
    best_cost: Dict[str, float] = {}

    while frontier:
        cost, _, state, path, actions_taken = heapq.heappop(frontier)

        if state in best_cost and best_cost[state] <= cost:
            continue
        best_cost[state] = cost

        if problem.goal_test(state):
            return {
                "path": path,
                "actions": actions_taken,
                "total_cost": cost,
            }

        for edge in problem.possible_actions(state):
            if edge.target not in best_cost or cost + edge.cost < best_cost.get(edge.target, float("inf")):
                counter += 1
                heapq.heappush(frontier, (
                    cost + edge.cost,
                    counter,
                    edge.target,
                    path + [edge.target],
                    actions_taken + [(edge.action, edge.cost)],
                ))

    return None


def describe_state_space(problem: PlanningProblem) -> str:
    """Human-readable printout of the full state-space graph."""
    lines = [f"Initial State: {problem.initial_state}", f"Goal State: {problem.goal_state}", "", "State-Space Graph:"]
    for state, edges in problem.state_space().items():
        if not edges:
            lines.append(f"  {state}  (no outgoing actions)")
            continue
        for action, target, cost in edges:
            lines.append(f"  {state} --[{action}, cost={cost}]--> {target}")
    return "\n".join(lines)


def describe_solution(result: dict, unit: str = "min") -> str:
    """Human-readable printout of the planned execution sequence."""
    if result is None:
        return "No plan found — goal state is unreachable from the initial state."

    lines = ["Planned Execution Sequence:"]
    running_total = 0.0
    lines.append(f"  {result['path'][0]}")
    for (action, cost), next_state in zip(result["actions"], result["path"][1:]):
        running_total += cost
        lines.append(f"    --[{action}, {cost} {unit}]--> {next_state}  (cumulative: {running_total} {unit})")
    lines.append(f"\nTotal Path Cost: {result['total_cost']} {unit}")
    return "\n".join(lines)
