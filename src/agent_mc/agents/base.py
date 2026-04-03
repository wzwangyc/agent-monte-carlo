"""
Agent Base Module - Agent 抽象基类

This module defines the core Agent interface that all agent types must implement.

Business Intent:
    Provide a unified interface for heterogeneous agents in the simulation.
    Enable plug-and-play agent types with consistent behavior.

Design Boundaries:
    - Abstract base class enforces interface contract
    - State and memory are separate dataclasses
    - Learning is optional (default: no-op)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import numpy as np


@dataclass
class AgentState:
    """
    Agent 内部状态
    
    Business Intent:
        Track agent's current financial position.
        
    Design Boundaries:
        - Immutable after creation (use update methods)
        - All values use float for consistency
        - Holdings tracked as symbol -> quantity mapping
    """
    
    cash: float = 100000.0
    """Available cash for trading"""
    
    holdings: Dict[str, int] = field(default_factory=dict)
    """Current holdings: {symbol: quantity}"""
    
    wealth: float = 100000.0
    """Total wealth (cash + market value of holdings)"""
    
    def update_wealth(self, current_prices: Dict[str, float]) -> None:
        """Update total wealth based on current prices."""
        market_value = sum(
            qty * current_prices.get(symbol, 0)
            for symbol, qty in self.holdings.items()
        )
        self.wealth = self.cash + market_value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'cash': self.cash,
            'holdings': self.holdings.copy(),
            'wealth': self.wealth
        }


@dataclass
class Experience:
    """
    单次交易经验
    
    Business Intent:
        Store complete experience for learning and analysis.
        
    Design Boundaries:
        - Immutable record of what happened
        - Includes all components for RL (state, action, reward, next_state)
    """
    
    timestamp: int
    observation: Dict[str, Any]
    action: Dict[str, Any]
    reward: float
    next_observation: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp,
            'observation': self.observation,
            'action': self.action,
            'reward': self.reward,
            'next_observation': self.next_observation
        }


@dataclass
class AgentMemory:
    """
    Agent 记忆系统
    
    Business Intent:
        Store historical experiences for learning and analysis.
        Support different time scales (short-term vs long-term).
        
    Design Boundaries:
        - Short-term: recent experiences (bounded deque)
        - Long-term: important events only
        - Statistics: aggregated metrics
    """
    
    short_term: List[Experience] = field(default_factory=list)
    """Recent experiences (bounded by max_size)"""
    
    long_term: List[Experience] = field(default_factory=list)
    """Important events (large rewards)"""
    
    statistics: Dict[str, float] = field(default_factory=dict)
    """Aggregated statistics"""
    
    max_size: int = 1000
    """Maximum short-term memory size"""
    
    important_threshold: float = 0.1
    """Threshold for storing in long-term memory"""
    
    def add_experience(self, experience: Experience) -> None:
        """Add experience to memory."""
        # Add to short-term
        self.short_term.append(experience)
        
        # Trim if needed
        if len(self.short_term) > self.max_size:
            self.short_term = self.short_term[-self.max_size:]
        
        # Add to long-term if important
        if abs(experience.reward) > self.important_threshold:
            self.long_term.append(experience)
        
        # Update statistics
        self._update_statistics()
    
    def _update_statistics(self) -> None:
        """Update aggregated statistics."""
        if not self.short_term:
            return
        
        rewards = [exp.reward for exp in self.short_term]
        self.statistics = {
            'total_experiences': len(self.short_term),
            'total_reward': sum(rewards),
            'avg_reward': np.mean(rewards),
            'std_reward': np.std(rewards),
            'win_rate': np.mean([r > 0 for r in rewards]),
            'max_reward': max(rewards),
            'min_reward': min(rewards)
        }
    
    def get_recent_observations(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get last n observations."""
        return [exp.observation for exp in self.short_term[-n:]]
    
    def sample_batch(self, batch_size: int = 32) -> List[Experience]:
        """Sample random batch for experience replay."""
        if len(self.short_term) <= batch_size:
            return self.short_term.copy()
        
        indices = np.random.choice(len(self.short_term), batch_size, replace=False)
        return [self.short_term[i] for i in sorted(indices)]
    
    def get_statistics(self) -> Dict[str, float]:
        """Get current statistics."""
        return self.statistics.copy()
    
    def clear(self) -> None:
        """Clear all memory."""
        self.short_term.clear()
        self.long_term.clear()
        self.statistics.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'short_term_count': len(self.short_term),
            'long_term_count': len(self.long_term),
            'statistics': self.statistics
        }


class Agent(ABC):
    """
    Agent 抽象基类
    
    Business Intent:
        Define the interface for all agent types in the simulation.
        Enable heterogeneous agents with different strategies.
        
    Design Boundaries:
        - All agents must implement perceive(), decide(), act()
        - Learning is optional (default: no-op)
        - State and memory are managed by base class
        - Random number generator for reproducibility
    
    Example:
        >>> class MyAgent(Agent):
        ...     def perceive(self, obs):
        ...         self.memory.add(obs)
        ...     
        ...     def decide(self):
        ...         return {'action': 'buy', 'quantity': 10}
        ...     
        ...     def act(self, decision):
        ...         return Order(...)
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        config: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None
    ):
        """
        Initialize agent.
        
        Args:
            agent_id: Unique identifier
            agent_type: Type name (e.g., 'momentum', 'value')
            config: Agent-specific configuration
            seed: Random seed for reproducibility
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config or {}
        
        # State and memory
        self.state = AgentState()
        self.memory = AgentMemory(
            max_size=self.config.get('memory_size', 1000),
            important_threshold=self.config.get('important_threshold', 0.1)
        )
        
        # Random number generator
        self.rng = np.random.default_rng(seed)
        
        # Metadata
        self.created_at = datetime.now()
        self.is_active = True
    
    @abstractmethod
    def perceive(self, observation: Dict[str, Any]) -> None:
        """
        感知环境
        
        Business Intent:
            Process environmental observation and update internal state.
            
        Args:
            observation: Environment state (prices, indicators, etc.)
        
        Example:
            >>> agent.perceive({
            ...     'price': 100.0,
            ...     'volume': 1000000,
            ...     'indicators': {...}
            ... })
        """
        pass
    
    @abstractmethod
    def decide(self) -> Dict[str, Any]:
        """
        做出决策
        
        Business Intent:
            Decide what action to take based on observations and memory.
            
        Returns:
            Decision dictionary with action details
        
        Example:
            >>> decision = agent.decide()
            >>> print(decision)
            {'action': 'buy', 'quantity': 10, 'price_limit': 101.0}
        """
        pass
    
    @abstractmethod
    def act(self, decision: Dict[str, Any]) -> Optional[Any]:
        """
        执行动作
        
        Business Intent:
            Convert decision into executable action (order).
            
        Args:
            decision: Output from decide()
            
        Returns:
            Executable action (e.g., Order object) or None
        """
        pass
    
    def learn(self, reward: Optional[float] = None) -> None:
        """
        从经验中学习
        
        Business Intent:
            Update strategy based on outcomes.
            
        Args:
            reward: Reward signal (optional, agent-specific)
        
        Note:
            Default implementation is no-op.
            Subclasses should override to implement learning.
        """
        pass
    
    def update_state(self, trade_result: Dict[str, Any]) -> None:
        """
        更新状态
        
        Business Intent:
            Update agent state after trade execution.
            
        Args:
            trade_result: Trade execution details
        """
        # Update cash
        if 'cash_change' in trade_result:
            self.state.cash += trade_result['cash_change']
        
        # Update holdings
        if 'symbol' in trade_result and 'quantity_change' in trade_result:
            symbol = trade_result['symbol']
            qty_change = trade_result['quantity_change']
            
            current_qty = self.state.holdings.get(symbol, 0)
            new_qty = current_qty + qty_change
            
            if new_qty == 0:
                self.state.holdings.pop(symbol, None)
            else:
                self.state.holdings[symbol] = new_qty
        
        # Update wealth
        if 'current_prices' in trade_result:
            self.state.update_wealth(trade_result['current_prices'])
    
    def reset(self) -> None:
        """
        重置 Agent
        
        Business Intent:
            Reset to initial state (for new simulation run).
        """
        self.state = AgentState()
        self.memory.clear()
        self.is_active = True
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取 Agent 信息
        
        Returns:
            Dictionary with agent metadata and current state
        """
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'config': self.config,
            'state': self.state.to_dict(),
            'memory': self.memory.to_dict(),
            'created_at': str(self.created_at),
            'is_active': self.is_active
        }
    
    def __repr__(self) -> str:
        return f"{self.agent_type}Agent(id={self.agent_id}, wealth={self.state.wealth:.2f})"
