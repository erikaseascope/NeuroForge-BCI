from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

from .state import GraphState
from ..agents.decoding import create_decoding_agent
from ..agents.biocompatibility import create_biocompatibility_agent
from ..agents.signal_processing import create_signal_processing_agent
from ..agents.firmware import create_firmware_agent
from ..security.dasr import enforce_dasr, DASRError
from ..security.audit import log_audit

# Placeholder LLM - replace with real one (Grok, OpenAI, etc.) later
from langchain_core.language_models import BaseLanguageModel
dummy_llm = None  # type: ignore  # Will be injected

decoding_agent = create_decoding_agent(dummy_llm)
signal_processing_agent = create_signal_processing_agent(dummy_llm)  # same dummy LLM placeholder
firmware_agent = create_firmware_agent(dummy_llm)  # using the same dummy LLM placeholder

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

biocompatibility_agent = create_biocompatibility_agent(dummy_llm)  # same dummy LLM placeholder

def biocompatibility_node(state: GraphState) -> Dict[str, Any]:
    """Run the Biocompatibility Cluster agent"""
    try:
        enforce_dasr(state)
    except DASRError as e:
        log_audit(f"Biocompatibility blocked: {str(e)}")
        return {
            "safety_flags": state["safety_flags"] + [str(e)],
            "requires_hitl": True,
            "audit_entries": state["audit_entries"] + [{"action": "biocompatibility_blocked"}]
        }

    log_audit("Biocompatibility agent invoked")
    
    agent_input = {
        "goal": state["goal"],
        "current_design": state.get("current_design", {}),
        "safety_flags": state["safety_flags"],
    }
    
    try:
        output = biocompatibility_agent.invoke(agent_input)
    except Exception as e:
        log_audit(f"Biocompatibility error: {str(e)}")
        output = f"Agent failed: {str(e)}"
    
    return {
        "messages": state["messages"] + [f"Biocompatibility proposal: {output}"],
        "iteration": state["iteration"] + 1,  # or keep same if parallel
        "current_design": state.get("current_design", {}) | {"biocompatibility_update": "improved_stability"},
        "audit_entries": state["audit_entries"] + [{"action": "biocompatibility_ran"}],
        "metrics": state["metrics"] | {"stability_score": 0.90}  # placeholder
    }

def signal_processing_node(state: GraphState) -> Dict[str, Any]:
    """Run the Signal Processing Cluster agent"""
    try:
        enforce_dasr(state)
    except DASRError as e:
        log_audit(f"Signal Processing blocked: {str(e)}")
        return {
            "safety_flags": state["safety_flags"] + [str(e)],
            "requires_hitl": True,
            "audit_entries": state["audit_entries"] + [{"action": "signal_processing_blocked"}]
        }

    log_audit("Signal Processing agent invoked")
    
    agent_input = {
        "goal": state["goal"],
        "current_design": state.get("current_design", {}),
        "safety_flags": state["safety_flags"],
    }
    
    try:
        output = signal_processing_agent.invoke(agent_input)
    except Exception as e:
        log_audit(f"Signal Processing error: {str(e)}")
        output = f"Agent failed: {str(e)}"
    
    return {
        "messages": state["messages"] + [f"Signal Processing proposal: {output}"],
        "iteration": state["iteration"] + 1,
        "current_design": state.get("current_design", {}) | {"signal_processing_update": "improved_noise_rejection"},
        "audit_entries": state["audit_entries"] + [{"action": "signal_processing_ran"}],
        "metrics": state["metrics"] | {"input_noise_uvrms": 4.2, "snr_db": 28.5}  # placeholder metrics
    }

def firmware_node(state: GraphState) -> Dict[str, Any]:
    """Run the Firmware & Embedded Systems Cluster agent"""
    try:
        enforce_dasr(state)
    except DASRError as e:
        log_audit(f"Firmware blocked: {str(e)}")
        return {
            "safety_flags": state["safety_flags"] + [str(e)],
            "requires_hitl": True,
            "audit_entries": state["audit_entries"] + [{"action": "firmware_blocked"}]
        }

    log_audit("Firmware agent invoked")
    
    agent_input = {
        "goal": state["goal"],
        "current_design": state.get("current_design", {}),
        "safety_flags": state["safety_flags"],
    }
    
    try:
        output = firmware_agent.invoke(agent_input)
    except Exception as e:
        log_audit(f"Firmware error: {str(e)}")
        output = f"Agent failed: {str(e)}"
    
    return {
        "messages": state["messages"] + [f"Firmware proposal: {output}"],
        "iteration": state["iteration"] + 1,
        "current_design": state.get("current_design", {}) | {
            "firmware_update": "added_safety_interlocks",
            "power_estimate_μW": 8.5
        },
        "audit_entries": state["audit_entries"] + [{"action": "firmware_ran"}],
        "metrics": state["metrics"] | {"telemetry_efficiency": 0.94}
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
    workflow.add_node("biocompatibility_agent", biocompatibility_node)
    workflow.add_node("signal_processing_agent", signal_processing_node)
    workflow.add_node("firmware_agent", firmware_node)
    workflow.add_node("governor", governor_node)

      # Example sequential pipeline: clean signal → decode → biocompatibility → firmware → governor
    workflow.add_edge(START, "safety_guard")
    workflow.add_edge("safety_guard", "signal_processing_agent")
    workflow.add_edge("signal_processing_agent", "decoding_agent")
    workflow.add_edge("decoding_agent", "biocompatibility_agent")
    workflow.add_edge("biocompatibility_agent", "firmware_agent")          # ← new
    workflow.add_edge("firmware_agent", "governor")
    
    # Keep your existing conditional edges from governor / agent
    # If you have a route_after_agent function, you can update it to include "firmware_agent" as an option
        route_after_agent,
        {
            "safety_guard": "safety_guard",  # loop
            "governor": "governor",
            "hitl_gate": "hitl_gate",        # placeholder node
            "__end__": END
        }
    )
    
    workflow.add_edge("governor", "safety_guard")  # continue loop unless killed

       # Improved HITL simulation node
    def hitl_gate_node(state: GraphState) -> Dict[str, Any]:
        log_audit("HITL gate reached - simulation mode")
        # In real UI: show state and wait for button click
        # Here: auto-approve for demo, or force pause
        simulated_approval = True  # Change to False to test rejection flow
        if simulated_approval:
            return {
                "hitl_approved": True,
                "requires_hitl": False,
                "messages": state["messages"] + ["HITL (simulated): Approved continuation"],
                "audit_entries": state["audit_entries"] + [{"action": "hitl_approved"}]
            }
        else:
            return {
                "messages": state["messages"] + ["HITL (simulated): Rejected - stopping"],
                "audit_entries": state["audit_entries"] + [{"action": "hitl_rejected"}]
            }

    workflow.add_node("hitl_gate", hitl_gate_node)
    workflow.add_edge("hitl_gate", END)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

if __name__ == "__main__":
    graph = build_neuroforge_graph()
    print("NeuroForge graph compiled with decoding agent connected.")
