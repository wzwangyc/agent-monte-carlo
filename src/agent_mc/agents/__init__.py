"""
Agent Module - 多智能体系统

This module provides the agent framework for Agent Monte Carlo.

Components:
    - base: Agent base class and state/memory dataclasses
    - memory: Advanced memory systems
    - learning: Learning algorithms (Q-learning, evolutionary)
    - types: Concrete agent implementations
"""

from .base import Agent, AgentState, AgentMemory, Experience

__all__ = [
    'Agent',
    'AgentState',
    'AgentMemory',
    'Experience',
]
