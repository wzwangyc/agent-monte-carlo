"""
Unit tests for domain types (Money, Price, Quantity, PnL, Return).

Coverage Requirements:
    - All constructors: 100%
    - Validation logic: 100%
    - Arithmetic operations: 100%
    - Edge cases: All boundary conditions
"""

import pytest
from decimal import Decimal

from agent_mc.types import Money, Price, Quantity, PnL, Return


class TestMoney:
    """Unit tests for Money class."""

    def test_valid_construction(self):
        """Valid Money construction should succeed."""
        money = Money(Decimal("1000.00"), "USD")
        assert money.amount == Decimal("1000.00")
        assert money.currency == "USD"

    def test_negative_amount(self):
        """Negative amount should be allowed (for PnL)."""
        # Note: Money allows negative for PnL use cases
        money = Money(Decimal("-500.00"), "USD")
        assert money.amount == Decimal("-500.00")

    def test_invalid_currency(self):
        """Invalid currency should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid currency"):
            Money(Decimal("100.00"), "INVALID")

    def test_non_decimal_amount(self):
        """Non-Decimal amount should raise TypeError."""
        with pytest.raises(TypeError, match="Amount must be Decimal"):
            Money(100.0, "USD")  # type: ignore

    def test_precision_normalization(self):
        """Amount should be normalized to 2 decimal places."""
        money = Money(Decimal("100.123456"), "USD")
        assert money.amount == Decimal("100.12")

    def test_addition_same_currency(self):
        """Adding same currency should succeed."""
        m1 = Money(Decimal("100.00"), "USD")
        m2 = Money(Decimal("50.00"), "USD")
        result = m1 + m2
        assert result.amount == Decimal("150.00")

    def test_addition_different_currency(self):
        """Adding different currencies should raise ValueError."""
        m1 = Money(Decimal("100.00"), "USD")
        m2 = Money(Decimal("50.00"), "EUR")
        with pytest.raises(ValueError, match="Cannot add"):
            m1 + m2

    def test_string_format(self):
        """String formatting should include currency symbol."""
        money = Money(Decimal("1234567.89"), "USD")
        assert str(money) == "$1,234,567.89"


class TestPrice:
    """Unit tests for Price class."""

    def test_valid_construction(self):
        """Valid Price construction should succeed."""
        price = Price(Decimal("152.3400"))
        assert price.value == Decimal("152.3400")

    def test_negative_price(self):
        """Negative price should raise ValueError."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Price(Decimal("-100.00"))

    def test_zero_price(self):
        """Zero price should raise ValueError."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Price(Decimal("0.00"))

    def test_precision_normalization(self):
        """Price should be normalized to 4 decimal places."""
        price = Price(Decimal("152.3456789"))
        assert price.value == Decimal("152.3457")

    def test_float_conversion(self):
        """Float conversion should work for research use."""
        price = Price(Decimal("152.3400"))
        assert float(price) == 152.34


class TestQuantity:
    """Unit tests for Quantity class."""

    def test_valid_construction(self):
        """Valid Quantity construction should succeed."""
        qty = Quantity(Decimal("100"))
        assert qty.value == Decimal("100")

    def test_negative_not_allowed(self):
        """Negative quantity should raise ValueError by default."""
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            Quantity(Decimal("-100"))

    def test_negative_allowed_for_shorts(self):
        """Negative quantity allowed with allow_negative=True."""
        qty = Quantity(Decimal("-100"), allow_negative=True)
        assert qty.value == Decimal("-100")

    def test_precision_normalization(self):
        """Quantity should be normalized to 8 decimal places."""
        qty = Quantity(Decimal("0.123456789"))
        assert qty.value == Decimal("0.12345679")


class TestPnL:
    """Unit tests for PnL class."""

    def test_profit(self):
        """Positive PnL should format correctly."""
        pnl = PnL(Money(Decimal("15234.56"), "USD"), realized=True)
        assert "+$15,234.56" in str(pnl)
        assert "realized" in str(pnl)

    def test_loss(self):
        """Negative PnL should format correctly."""
        pnl = PnL(Money(Decimal("-5000.00"), "USD"), realized=False)
        assert "-$5,000.00" in str(pnl)
        assert "unrealized" in str(pnl)


class TestReturn:
    """Unit tests for Return class."""

    def test_valid_construction(self):
        """Valid Return construction should succeed."""
        ret = Return(Decimal("0.0523"))
        assert ret.value == Decimal("0.0523")

    def test_percentage_format(self):
        """Percentage formatting should work."""
        ret = Return(Decimal("0.0523"))
        assert ret.as_percentage() == "5.23%"

    def test_negative_return(self):
        """Negative return should be allowed."""
        ret = Return(Decimal("-0.1234"))
        assert ret.as_percentage() == "-12.34%"

    def test_total_loss(self):
        """-100% return should be allowed (total loss)."""
        ret = Return(Decimal("-1.0"))
        assert ret.as_percentage() == "-100.00%"

    def test_beyond_total_loss(self):
        """Return < -100% should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be less than -100%"):
            Return(Decimal("-1.5"))

    def test_precision_normalization(self):
        """Return should be normalized to 6 decimal places."""
        ret = Return(Decimal("0.0523456789"))
        assert ret.value == Decimal("0.052346")
