from typing import TypedDict, Annotated, List, Optional
from langchain_core.messages import BaseMessage
import operator


class GraphState(TypedDict):
    """
    Shared state passed between nodes in the NeuroForge recursive graph.
    Keeps track of the current design iteration, decisions, safety flags, etc.
    """
    # Main design goal / prompt from user or previous iteration
    goal: str

    # Current iteration number (increases on each recursive loop)
    iteration: int

    # Accumulated messages / thoughts from agents
    messages: Annotated[List[BaseMessage], operator.add]

    # Current best proposed design (JSON-like dict, evolves over iterations)
    current_design: dict

    # Safety & risk flags (raised by security layer or agents)
    safety_flags: List[str]

    # Whether human review is required before next step
    requires_hitl: bool

    # Abstracted metrics from simulations (bits/s, stability projection, etc.)
    metrics: dict

    # Final certified status (only set after full validation loop)
    certified: Optional[bool]

    # Audit trail entry (appended by security layer)
    audit_entries: Annotated[List[dict], operator.add]
