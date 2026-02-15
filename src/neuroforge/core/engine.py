from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

from .state import GraphState
from ..agents.decoding import create_decoding_agent
from ..security.dasr import enforce_dasr, DASRError
from ..security.audit import log_audit

# Placeholder LLM - replace with real one (Grok, OpenAI, etc.) later
from langchain_core.language_models import BaseLanguageModel
dummy_llm = None  # type: ignore  # Will be injected

decoding_agent = create_decoding_agent(dummy_llm)

def decoding_node(state: GraphState) -> Dict[str, Any]:
    """Run the Decoding Cluster agent"""
    try:
        enforce_dasr(state)  # DASR check before agent runs
    except DASRError as e:
        log_audit(f"Decoding blocked: {str(e)}")
        return {
            "safety_flags": state["safety_flags"] + [str(e)],
            "requires_hitl": True,
            "audit_entries": state["audit_entries"] + [{"action": "decoding_blocked"}]
        }

    log_audit("Decoding agent invoked")
    
    # Invoke agent (placeholder input - expand later)
    agent_input = {
        "goal": state["goal"],
        "current_design": state.get("current_design", {}),
        "safety_flags": state["safety_flags"],
    }
    
    try:
        output = decoding_agent.invoke(agent_input)
    except Exception as e:
        log_audit(f"Decoding error: {str(e)}")
        output = f"Agent failed: {str(e)}"
    
    return {
        "messages": state["messages"] + [f"Decoding proposal: {output}"],
        "iteration": state["iteration"] + 1,
        "current_design": state.get("current_design", {}) | {"decoding_update": "placeholder_improvement"},
        "audit_entries": state["audit_entries"] + [{"action": "decoding_ran"}]
    }

def safety_guard_node(state: GraphState) -> Dict[str, Any]:
    """Security envelope check"""
    log_audit("Running safety guard")
    new_flags = []
    # Simple example rule
    if "degradation > 20%" in str(state.get("current_design", {})):
        new_flags.append("Chronic degradation risk HIGH")
    
    requires_hitl = len(new_flags) > 0 or state["iteration"] >= 5
    
    return {
        "safety_flags": state["safety_flags"] + new_flags,
        "requires_hitl": requires_hitl,
        "audit_entries": state["audit_entries"] + [{
            "timestamp": "placeholder",
            "action": "safety_guard",
            "result": "passed" if not new_flags else "flags"
        }]
    }

def governor_node(state: GraphState) -> Dict[str, Any]:
    """Governor: enforce compute limits, alignment, kill-switch"""
    log_audit("Governor check")
    if state["iteration"] > 10:
        return {"requires_hitl": True, "messages": state["messages"] + ["Governor: Max iterations reached - HITL required"]}
    return {}

def route_after_agent(state: GraphState) -> Literal["safety_guard", "governor", "hitl_gate", "__end__"]:
    """Router for conditional edges"""
    if state["requires_hitl"]:
        return "hitl_gate"
    if state["iteration"] >= 10:
        return "__end__"
    return "governor"  # or back to safety/agent loop

# Build graph
def build_neuroforge_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("safety_guard", safety_guard_node)
    workflow.add_node("decoding_agent", decoding_node)
    workflow.add_node("governor", governor_node)

    workflow.add_edge(START, "safety_guard")
    workflow.add_edge("safety_guard", "decoding_agent")
    
    workflow.add_conditional_edges(
        "decoding_agent",
        route_after_agent,
        {
            "safety_guard": "safety_guard",  # loop
            "governor": "governor",
            "hitl_gate": "hitl_gate",        # placeholder node
            "__end__": END
        }
    )
    
    workflow.add_edge("governor", "safety_guard")  # continue loop unless killed

    # Placeholder HITL node (expand later)
    def hitl_gate_node(state):
        return {"messages": state["messages"] + ["Paused for HITL review"]}

    workflow.add_node("hitl_gate", hitl_gate_node)
    workflow.add_edge("hitl_gate", END)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

if __name__ == "__main__":
    graph = build_neuroforge_graph()
    print("NeuroForge graph compiled with decoding agent connected.")
