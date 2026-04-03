"""
Agent Monte Carlo - Enterprise-grade agent-based Monte Carlo simulation framework.

This package provides a hybrid simulation engine combining traditional Monte Carlo
computational efficiency with Agent-Based Modeling (ABM) behavioral realism.

Key Features:
    - Adaptive regime switching between MC and ABM modes
    - Automated Bayesian parameter calibration
    - SHAP-based explainability
    - 5-layer validation framework
    - GPU acceleration support

Example:
    >>> from agent_mc import AgentMonteCarloSimulator, Config
    >>> config = Config(n_simulations=10000, confidence_level=0.95)
    >>> simulator = AgentMonteCarloSimulator(config)
    >>> results = simulator.run(data)
"""

__version__ = "0.5.0"
__author__ = "Agent Monte Carlo Contributors"
__email__ = "agent-mc@example.com"

from agent_mc.config import Config
from agent_mc.simulator import AgentMonteCarloSimulator
from agent_mc.types import Money, Price, Quantity, PnL, Return

__all__ = [
    "AgentMonteCarloSimulator",
    "Config",
    "Money",
    "Price",
    "Quantity",
    "PnL",
    "Return",
]
