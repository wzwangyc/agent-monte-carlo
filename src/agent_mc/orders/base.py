"""
Order and Trade Base Classes - 订单和交易基础类

This module defines the core data structures for orders and trades.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid


@dataclass
class Order:
    """
    交易订单
    
    Attributes:
        order_id: Unique order identifier
        agent_id: ID of the agent placing the order
        side: 'buy' or 'sell'
        quantity: Number of shares
        price: Limit price (None for market orders)
        order_type: 'limit', 'market', or 'stop'
        timestamp: Order creation time
    """
    
    agent_id: str
    side: str  # 'buy' or 'sell'
    quantity: int
    price: Optional[float] = None
    order_type: str = 'limit'
    timestamp: datetime = field(default_factory=datetime.now)
    order_id: str = field(default_factory=lambda: f"ORD_{uuid.uuid4().hex[:8]}")
    
    def __post_init__(self):
        """Validate order"""
        assert self.side in ['buy', 'sell'], f"Invalid side: {self.side}"
        assert self.quantity > 0, f"Quantity must be positive: {self.quantity}"
        assert self.order_type in ['limit', 'market', 'stop'], f"Invalid type: {self.order_type}"
        
        if self.order_type == 'limit' and self.price is None:
            raise ValueError("Limit order must have a price")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'order_id': self.order_id,
            'agent_id': self.agent_id,
            'side': self.side,
            'quantity': self.quantity,
            'price': self.price,
            'order_type': self.order_type,
            'timestamp': str(self.timestamp)
        }


@dataclass
class Trade:
    """
    成交记录
    
    Attributes:
        trade_id: Unique trade identifier
        price: Execution price
        quantity: Executed quantity
        buyer_id: ID of buying agent
        seller_id: ID of selling agent
        buyer_order_id: ID of buyer's order
        seller_order_id: ID of seller's order
        timestamp: Execution time
    """
    
    price: float
    quantity: int
    buyer_id: str
    seller_id: str
    buyer_order_id: str
    seller_order_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    trade_id: str = field(default_factory=lambda: f"TRD_{uuid.uuid4().hex[:8]}")
    
    def __post_init__(self):
        """Validate trade"""
        assert self.price > 0, f"Price must be positive: {self.price}"
        assert self.quantity > 0, f"Quantity must be positive: {self.quantity}"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'trade_id': self.trade_id,
            'price': self.price,
            'quantity': self.quantity,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'buyer_order_id': self.buyer_order_id,
            'seller_order_id': self.seller_order_id,
            'timestamp': str(self.timestamp)
        }
