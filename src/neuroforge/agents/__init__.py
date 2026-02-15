"""
NeuroForge Agents Package
BCI-specific agent clusters (decoding, biocompatibility, etc.)
"""

# Explicit exports for cleaner imports
from .decoding import create_decoding_agent
from .biocompatibility import create_biocompatibility_agent

__all__ = [
    "create_decoding_agent",
    "create_biocompatibility_agent",
    # Add more agents here as implemented (e.g., "create_surgical_robotics_agent")
]
