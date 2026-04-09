"""Shared agent state definition for the lawyer agent graph."""

from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


LawCategory = Literal["civil", "criminal", "administrative", "family", "unknown"]


class AgentState(TypedDict):
    """State shared across all nodes in the lawyer agent graph."""

    # Conversation messages (HumanMessage / AIMessage)
    messages: Annotated[list, add_messages]

    # Law category determined by the router node
    category: LawCategory
