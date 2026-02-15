"""
NeuroForge - Recursive AI Swarm for Safe BCI Engineering
"""

__version__ = "0.1.0"

from .core.engine import build_neuroforge_graph
from .ui.dashboard import main as run_dashboard  # if you add def main() later

__all__ = ["build_neuroforge_graph", "run_dashboard"]
