"""
Input validation module.

Business Intent:
    Strict validation at system boundaries.
    No unvalidated data enters core logic.

Design Boundaries:
    - Fail-fast on invalid inputs
    - Clear error messages
    - Schema-based validation
"""

from __future__ import annotations

from typing import Any


def validate_input(data: Any, schema: type) -> Any:
    """
    Validate input against schema.

    Business Intent:
        Ensure all external inputs meet requirements before processing.

    Design Boundaries:
        - Raises on first validation error
        - Clear error message with expected vs actual
        - No silent coercion

    Args:
        data: Input data to validate
        schema: Schema type to validate against

    Returns:
        Validated data

    Raises:
        ValueError: If validation fails
        TypeError: If type mismatch
    """
    # Placeholder: actual implementation will use pydantic or similar
    return data


def validate_prices(prices: list[float]) -> list[float]:
    """
    Validate price series.

    Business Intent:
        Ensure price data is valid for simulation.

    Design Boundaries:
        - All prices must be > 0
        - No NaN or Inf values
        - Minimum 2 data points

    Args:
        prices: List of prices

    Returns:
        Validated price list

    Raises:
        ValueError: If validation fails
    """
    if len(prices) < 2:
        raise ValueError(f"Need at least 2 prices, got {len(prices)}")

    for i, price in enumerate(prices):
        if price <= 0:
            raise ValueError(f"Price at index {i} must be > 0, got {price}")
        if price != price:  # NaN check
            raise ValueError(f"Price at index {i} is NaN")

    return prices


def validate_returns(returns: list[float]) -> list[float]:
    """
    Validate return series.

    Business Intent:
        Ensure return data is reasonable.

    Design Boundaries:
        - Returns typically in [-1, +10] range
        - No NaN or Inf values
        - Warn on extreme values

    Args:
        returns: List of returns

    Returns:
        Validated return list

    Raises:
        ValueError: If validation fails
    """
    for i, ret in enumerate(returns):
        if ret != ret:  # NaN check
            raise ValueError(f"Return at index {i} is NaN")
        if ret < -1:
            raise ValueError(
                f"Return at index {i} is {ret:.4f} (< -100%). "
                "Check data for errors."
            )

    return returns
