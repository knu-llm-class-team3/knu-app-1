"""LangGraph agent graph definition for the lawyer agent.

Graph structure:
    START
      │
      ▼
  router_node  ──── (category) ────┬─► civil_node
                                   ├─► criminal_node
                                   ├─► admin_node
                                   ├─► family_node
                                   └─► unknown_node
                                            │
                                            ▼
                                          END
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from nodes import (
    admin_node,
    civil_node,
    criminal_node,
    family_node,
    router_node,
    unknown_node,
)
from state import AgentState
from tools import search_case_law


def _route(state: AgentState) -> str:
    """Routing function: maps the detected category to the next node name."""
    return state.get("category", "unknown")


def build_graph() -> StateGraph:
    """Build and compile the lawyer agent graph."""
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("router", router_node)
    graph.add_node("civil", civil_node)
    graph.add_node("criminal", criminal_node)
    graph.add_node("administrative", admin_node)
    graph.add_node("family", family_node)
    graph.add_node("unknown", unknown_node)
    graph.add_node("tools", ToolNode([search_case_law]))

    # Entry edge
    graph.add_edge(START, "router")

    # Conditional routing from router to category nodes
    graph.add_conditional_edges(
        "router",
        _route,
        {
            "civil": "civil",
            "criminal": "criminal",
            "administrative": "administrative",
            "family": "family",
            "unknown": "unknown",
        },
    )

    # Each category node can call tools; tools routes back via state["category"]
    for category in ("civil", "criminal", "administrative", "family"):
        graph.add_conditional_edges(
            category,
            lambda s: "tools" if _has_tool_calls(s) else END,
            {"tools": "tools", END: END},
        )

    graph.add_conditional_edges(
        "tools",
        lambda s: s.get("category", "unknown"),
        {
            "civil": "civil",
            "criminal": "criminal",
            "administrative": "administrative",
            "family": "family",
            "unknown": "unknown",
        },
    )

    graph.add_edge("unknown", END)

    return graph.compile()


def _has_tool_calls(state: AgentState) -> bool:
    """Return True if the latest AI message contains tool call requests."""
    messages = state.get("messages", [])
    if not messages:
        return False
    last = messages[-1]
    return bool(getattr(last, "tool_calls", None))
