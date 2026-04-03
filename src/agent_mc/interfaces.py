"""
Abstract Interfaces - 依赖倒置层

This module defines abstract interfaces for market operations.
Agents depend on these interfaces, not concrete implementations.

Purpose:
- Eliminate circular dependencies
- Enable easy testing with mock implementations
- Support multiple market mechanisms
"""

from typing import Dict, Protocol, runtime_checkable


@runtime_checkable
class IMarketProvider(Protocol):
    """
    市场提供者接口
    
    All market mechanisms must implement this interface.
    Used by agents to interact with the market.
    """
    
    def get_quotes(self) -> Dict[str, float]:
        """
        Get current market quotes.
        
        Returns:
            Dictionary with 'bid', 'ask', 'spread', 'mid' prices
        """
        ...
    
    def execute_order(self, order: 'Order') -> 'Trade':
        """
        Execute a trading order.
        
        Args:
            order: Order object with side, quantity, price
            
        Returns:
            Trade object with execution details
        """
        ...
    
    def get_order_flow(self) -> float:
        """
        Get current net order flow.
        
        Returns:
            Net order flow (positive = net buying)
        """
        ...
    
    def get_current_price(self) -> float:
        """
        Get current market price.
        
        Returns:
            Current price (mid price or last trade price)
        """
        ...


@runtime_checkable
class IAgent(Protocol):
    """
    Agent 接口
    
    All agent types must implement this interface.
    Used by simulator to interact with agents.
    """
    
    @property
    def agent_id(self) -> str:
        """Unique agent identifier"""
        ...
    
    @property
    def agent_type(self) -> str:
        """Agent type (e.g., 'momentum', 'value')"""
        ...
    
    def perceive(self, observation: Dict) -> None:
        """Process market observation"""
        ...
    
    def decide(self) -> Dict:
        """Make trading decision"""
        ...
    
    def act(self, decision: Dict) -> 'Order':
        """Convert decision to order"""
        ...
    
    def learn(self, reward: float) -> None:
        """Learn from trading outcome"""
        ...


# Forward declarations to avoid circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .orders.base import Order, Trade
