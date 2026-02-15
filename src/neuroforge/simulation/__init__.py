"""
NeuroForge Simulation Package
Wrappers for Brian2, NEURON, PyBullet, etc. (synthetic only)
"""

from .neural_sim import run_synthetic_neural_sim

__all__ = ["run_synthetic_neural_sim"]
