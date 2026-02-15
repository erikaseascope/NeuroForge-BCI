"""
NeuroForge Agents Package
BCI-specific agent clusters (decoding, biocompatibility, etc.)
"""

# Optional: explicit exports (add more as you implement agents)
from .decoding import create_decoding_agent

__all__ = [
    "create_decoding_agent",
    # "create_biocompatibility_agent",  # etc. – uncomment/add later
]
