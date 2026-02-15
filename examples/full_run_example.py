"""
Full NeuroForge run example - console version (placeholder inputs)
Run with: python examples/full_run_example.py
"""

import os
from dotenv import load_dotenv

from neuroforge.core.engine import build_neuroforge_graph
from neuroforge.core.state import GraphState
from neuroforge.security.audit import log_audit

load_dotenv()

if __name__ == "__main__":
    print("NeuroForge Full Run Example (v0.1 placeholder)")
    
    initial_state: GraphState = {
        "goal": "Reduce chronic signal degradation by 30% in 6-month simulated implant",
        "iteration": 0,
        "messages": [],
        "current_design": {"electrode_count": 1024, "decoding_type": "adaptive_kalman"},
        "safety_flags": [],
        "requires_hitl": False,
        "metrics": {},
        "certified": None,
        "audit_entries": [],
        "hitl_approved": False,
    }
    
    graph = build_neuroforge_graph()
    
    # Run one cycle (expand to loop or stream later)
    config = {"configurable": {"thread_id": "example-run-1"}}
    final_state = graph.invoke(initial_state, config)
    
    print("\nFinal State Summary:")
    print(f"Iterations: {final_state['iteration']}")
    print(f"Safety flags: {final_state['safety_flags']}")
    print(f"Requires HITL: {final_state['requires_hitl']}")
    print(f"Messages: {final_state['messages'][-2:]}")  # last few
    print(f"Audit entries count: {len(final_state['audit_entries'])}")
    
    log_audit("Example run completed")
