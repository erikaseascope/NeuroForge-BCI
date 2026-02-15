"""
Basic unit tests for NeuroForge core state.
Run with: pytest tests/
"""

import pytest
from typing import List
from langchain_core.messages import HumanMessage

from neuroforge.core.state import GraphState


def test_graph_state_initialization():
    """Test basic GraphState creation and defaults"""
    state: GraphState = {
        "goal": "Test goal",
        "iteration": 0,
        "messages": [],
        "current_design": {},
        "safety_flags": [],
        "requires_hitl": False,
        "metrics": {},
        "certified": None,
        "audit_entries": [],
    }
    
    assert state["goal"] == "Test goal"
    assert state["iteration"] == 0
    assert len(state["messages"]) == 0
    assert state["requires_hitl"] is False


def test_graph_state_messages_append():
    """Test annotated add for messages"""
    state: GraphState = {
        "goal": "",
        "iteration": 0,
        "messages": [HumanMessage(content="Initial")],
        "current_design": {},
        "safety_flags": [],
        "requires_hitl": False,
        "metrics": {},
        "certified": None,
        "audit_entries": [],
    }
    
    new_messages: List = state["messages"] + [HumanMessage(content="New")]
    assert len(new_messages) == 2
    assert new_messages[-1].content == "New"


def test_invalid_state_missing_key():
    """Test that missing required keys raise issues (optional strict validation later)"""
    with pytest.raises(KeyError):
        state: GraphState = {"goal": "only this"}  # type: ignore
        _ = state["iteration"]  # Should fail
