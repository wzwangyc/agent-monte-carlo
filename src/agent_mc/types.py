"""
Domain types for financial values.

This module provides explicit, strongly-typed abstractions for financial quantities.
Following FAST.md standards:
- No raw primitives for financial meaning
- Explicit units, currency, and precision
- Fail-fast validation at construction

Business Intent:
    Financial calculations require exact arithmetic and explicit semantics.
    Using raw floats for money/PnL leads to rounding errors and semantic confusion.
    These types enforce correctness at the type system level.

Design Boundaries:
    - Money: Exact decimal values with currency
    - Price: Positive decimal values (asset prices)
    - Quantity: Non-negative integer or decimal (shares, contracts)
    - PnL: Signed decimal with currency (profit/loss)
    - Return: Dimensionless ratio (percentage as decimal)

Applicable Scenarios:
    - All production financial calculations
    - Risk management and reporting
    - Backtesting and live trading
    - NOT for research/statistical analysis (use float there)
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal, Union

# Currency codes (ISO 4217 subset)
CurrencyCode = Literal["USD", "EUR", "SGD", "CNY", "GBP", "JPY", "HKD"]


@dataclass(frozen=True)
class Money:
    """
    Explicit monetary value with currency and precision.

    Business Intent:
        Represents exact monetary amounts with proper decimal precision.
        Used for PnL, portfolio value, cash balances, etc.

    Design Boundaries:
        - Amount cannot be None
        - Currency must be valid ISO code
        - Precision fixed at 2 decimal places (cents)
        - Immutable (frozen dataclass)

    Example:
        >>> capital = Money(Decimal("1000000.00"), "USD")
        >>> pnl = Money(Decimal("15234.56"), "USD")
    """

    amount: Decimal
    currency: CurrencyCode = "USD"

    def __post_init__(self) -> None:
        """
        Validate and normalize monetary value.

        Fail-Fast Triggers:
            - amount is None or not a Decimal
            - amount is negative (for capital; PnL can be negative)
            - currency is not a valid ISO code

        Expected Behavior:
            Raises ValueError with clear message for invalid inputs.
        """
        # Validate amount type
        if not isinstance(self.amount, Decimal):
            raise TypeError(f"Amount must be Decimal, got {type(self.amount).__name__}")

        # Validate currency
        valid_currencies = {"USD", "EUR", "SGD", "CNY", "GBP", "JPY", "HKD"}
        if self.currency not in valid_currencies:
            raise ValueError(
                f"Invalid currency '{self.currency}'. "
                f"Must be one of: {', '.join(sorted(valid_currencies))}"
            )

        # Normalize to 2 decimal places
        object.__setattr__(
            self,
            "amount",
            self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        )

    def __str__(self) -> str:
        """Format as currency string (e.g., '$1,000,000.00')."""
        symbols = {
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "JPY": "¥",
            "CNY": "¥",
            "HKD": "HK$",
            "SGD": "S$",
        }
        symbol = symbols.get(self.currency, f"{self.currency} ")
        return f"{symbol}{self.amount:,.2f}"

    def __add__(self, other: Money) -> Money:
        """Add two Money values (must have same currency)."""
        if not isinstance(other, Money):
            raise TypeError(f"Can only add Money to Money, got {type(other).__name__}")
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add {self.currency} and {other.currency}. "
                "Convert to same currency first."
            )
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        """Subtract two Money values (must have same currency)."""
        if not isinstance(other, Money):
            raise TypeError(f"Can only subtract Money from Money, got {type(other).__name__}")
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot subtract {other.currency} from {self.currency}. "
                "Convert to same currency first."
            )
        return Money(self.amount - other.amount, self.currency)

    def __neg__(self) -> Money:
        """Negate monetary value (for PnL reversal)."""
        return Money(-self.amount, self.currency)


@dataclass(frozen=True)
class Price:
    """
    Asset price (positive decimal value).

    Business Intent:
        Represents the price of a financial asset (stock, bond, derivative).
        Must be strictly positive (zero price = delisted/worthless).

    Design Boundaries:
        - Value must be > 0
        - Precision at 4 decimal places (sufficient for most assets)
        - No currency (price is in quote currency of the instrument)

    Example:
        >>> stock_price = Price(Decimal("152.3400"))
        >>> fx_rate = Price(Decimal("1.0850"))
    """

    value: Decimal

    def __post_init__(self) -> None:
        """Validate price is positive."""
        if not isinstance(self.value, Decimal):
            raise TypeError(f"Price value must be Decimal, got {type(self.value).__name__}")
        if self.value <= 0:
            raise ValueError(f"Price must be positive, got {self.value}")

        # Normalize to 4 decimal places
        object.__setattr__(
            self,
            "value",
            self.value.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP),
        )

    def __str__(self) -> str:
        """Format price string."""
        return f"{self.value:.4f}"

    def __float__(self) -> float:
        """Convert to float (for research/statistical use only)."""
        return float(self.value)


@dataclass(frozen=True)
class Quantity:
    """
    Asset quantity (shares, contracts, units).

    Business Intent:
        Represents the amount of an asset held or traded.
        Can be integer (stocks) or decimal (crypto, forex).

    Design Boundaries:
        - Must be >= 0 for long positions
        - Negative allowed for short positions (explicit)
        - Precision at 8 decimal places (sufficient for crypto)

    Example:
        >>> shares = Quantity(Decimal("100"))  # 100 shares
        >>> crypto = Quantity(Decimal("0.12345678"))  # Bitcoin
    """

    value: Decimal
    allow_negative: bool = False  # Set True for short positions

    def __post_init__(self) -> None:
        """Validate quantity."""
        if not isinstance(self.value, Decimal):
            raise TypeError(f"Quantity value must be Decimal, got {type(self.value).__name__}")
        if not self.allow_negative and self.value < 0:
            raise ValueError(f"Quantity cannot be negative, got {self.value}")

        # Normalize to 8 decimal places
        object.__setattr__(
            self,
            "value",
            self.value.quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP),
        )

    def __str__(self) -> str:
        """Format quantity string."""
        # Remove trailing zeros
        normalized = self.value.normalize()
        return f"{normalized:f}"


@dataclass(frozen=True)
class PnL:
    """
    Profit and Loss (signed monetary value).

    Business Intent:
        Represents realized or unrealized profit/loss.
        Positive = profit, Negative = loss.

    Design Boundaries:
        - Can be positive or negative
        - Includes currency
        - Tracks realized vs unrealized

    Example:
        >>> pnl = PnL(Money(Decimal("15234.56"), "USD"), realized=True)
        >>> if pnl.value.amount > 0:
        ...     print(f"Profit: {pnl}")
    """

    value: Money
    realized: bool = True  # True = realized, False = unrealized

    def __str__(self) -> str:
        """Format PnL with sign."""
        sign = "+" if self.value.amount >= 0 else ""
        status = "realized" if self.realized else "unrealized"
        return f"{sign}{self.value} ({status})"


@dataclass(frozen=True)
class Return:
    """
    Investment return (dimensionless ratio).

    Business Intent:
        Represents return as a decimal ratio (e.g., 0.05 = 5% return).
        Used for performance metrics, risk calculations.

    Design Boundaries:
        - Dimensionless (no currency)
        - Can be positive or negative
        - Typically in range [-1, +inf] (-100% to +inf%)

    Example:
        >>> ret = Return(Decimal("0.0523"))  # 5.23% return
        >>> print(f"Return: {ret.as_percentage()}")
    """

    value: Decimal

    def __post_init__(self) -> None:
        """Validate return is in reasonable range."""
        if not isinstance(self.value, Decimal):
            raise TypeError(f"Return value must be Decimal, got {type(self.value).__name__}")
        if self.value < Decimal("-1"):
            raise ValueError(
                f"Return cannot be less than -100% (got {self.value:.4f}). "
                "Check calculation for errors."
            )

        # Normalize to 6 decimal places
        object.__setattr__(
            self,
            "value",
            self.value.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP),
        )

    def as_percentage(self) -> str:
        """Format as percentage string (e.g., '5.23%')."""
        return f"{float(self.value) * 100:.2f}%"

    def __str__(self) -> str:
        """Format return string."""
        return f"{self.value:.6f}"

    def __float__(self) -> float:
        """Convert to float (for research/statistical use only)."""
        return float(self.value)
