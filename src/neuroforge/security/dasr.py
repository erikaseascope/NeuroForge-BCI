"""
DASR (Data Access Security Rules) Envelope
Enforces least-privilege, no raw neural data, HITL gates, etc.
"""

from typing import Dict, Any
from .audit import log_audit

class DASRError(Exception):
    pass

def enforce_dasr(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check state before any agent call or graph step.
    Raise if violation detected.
    """
    if "raw_neural" in str(state).lower() or "patient_id" in str(state):
        log_audit("DASR violation: attempted raw sensitive data access")
        raise DASRError("DASR violation: No raw neural/patient data allowed")

    if state.get("requires_hitl", False) and not state.get("hitl_approved", False):
        log_audit("HITL gate blocked execution")
        raise DASRError("Human-in-the-Loop approval required")

    log_audit("DASR check passed")
    return state
