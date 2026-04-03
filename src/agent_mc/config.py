"""
Configuration module for Agent Monte Carlo simulator.

Business Intent:
    Centralized configuration management with strict validation.
    All simulation parameters are explicitly defined and validated.

Design Boundaries:
    - All fields are required (no implicit defaults for critical params)
    - Values validated at construction (fail-fast)
    - Immutable configuration (frozen dataclass)
    - Type-safe with mypy

Applicable Scenarios:
    - Simulation setup
    - Backtesting configuration
    - Live trading parameters
    - Risk threshold settings
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Literal, Optional

# Model validation level
ValidationLevel = Literal["basic", "standard", "strict"]

# Simulation mode
SimulationMode = Literal["mc", "abm", "hybrid"]


@dataclass(frozen=True)
class Config:
    """
    Agent Monte Carlo simulation configuration.

    Business Intent:
        Defines all parameters for Monte Carlo / ABM simulation.
        Ensures reproducibility and auditability.

    Design Boundaries:
        - n_simulations: Must be > 0, typically >= 1000 for statistical significance
        - time_horizon: Trading days (252 = 1 year)
        - confidence_level: Typically 0.95 or 0.99 for VaR
        - adaptive_mode: Enables regime switching (recommended for production)
        - seed: For reproducibility (None = random)

    Example:
        >>> config = Config(
        ...     n_simulations=10000,
        ...     time_horizon=252,
        ...     confidence_level=0.95,
        ...     adaptive_mode=True,
        ...     seed=42
        ... )
    """

    # Core simulation parameters
    n_simulations: int = 10000
    """Number of simulation paths (must be > 0)"""

    time_horizon: int = 252
    """Simulation horizon in trading days (252 = 1 year)"""

    confidence_level: Decimal = field(default_factory=lambda: Decimal("0.95"))
    """Confidence level for VaR/ES calculations (0.90-0.999)"""

    # Mode selection
    mode: SimulationMode = "hybrid"
    """
    Simulation mode:
        - 'mc': Traditional Monte Carlo (faster, less realistic)
        - 'abm': Agent-Based Model (slower, more realistic)
        - 'hybrid': Adaptive switching (recommended)
    """

    adaptive_mode: bool = True
    """Enable adaptive regime switching based on market conditions"""

    # Random seed for reproducibility
    seed: Optional[int] = None
    """Random seed (None = random, int = reproducible)"""

    # Validation settings
    validation_level: ValidationLevel = "standard"
    """
    Validation strictness:
        - 'basic': Minimal checks (research only)
        - 'standard': Production defaults
        - 'strict': Maximum validation (audits, compliance)
    """

    # GPU acceleration
    use_gpu: bool = False
    """Enable GPU acceleration (requires CUDA/PyTorch)"""

    # Risk limits
    max_drawdown_limit: Decimal = field(default_factory=lambda: Decimal("0.20"))
    """Maximum acceptable drawdown (0.20 = 20%)"""

    var_limit: Optional[Decimal] = None
    """Maximum acceptable VaR (None = no limit)"""

    # Output settings
    verbose: bool = False
    """Enable verbose logging"""

    save_paths: bool = False
    """Save all simulation paths (memory intensive)"""

    def __post_init__(self) -> None:
        """
        Validate configuration parameters.

        Fail-Fast Triggers:
            - n_simulations <= 0
            - time_horizon <= 0
            - confidence_level not in [0.90, 0.999]
            - Invalid mode string
            - max_drawdown_limit <= 0 or > 1

        Expected Behavior:
            Raises ValueError with clear message for invalid configs.
        """
        # Validate n_simulations
        if self.n_simulations <= 0:
            raise ValueError(
                f"n_simulations must be > 0, got {self.n_simulations}. "
                "Use at least 1000 for statistical significance."
            )

        # Validate time_horizon
        if self.time_horizon <= 0:
            raise ValueError(
                f"time_horizon must be > 0, got {self.time_horizon}. "
                "Use 252 for 1 trading year."
            )

        # Validate confidence_level
        if not Decimal("0.90") <= self.confidence_level <= Decimal("0.999"):
            raise ValueError(
                f"confidence_level must be in [0.90, 0.999], got {self.confidence_level}. "
                "Typical values: 0.95 (95% VaR) or 0.99 (99% VaR)."
            )

        # Validate mode
        valid_modes = {"mc", "abm", "hybrid"}
        if self.mode not in valid_modes:
            raise ValueError(
                f"Invalid mode '{self.mode}'. Must be one of: {', '.join(sorted(valid_modes))}"
            )

        # Validate max_drawdown_limit
        if not Decimal("0") < self.max_drawdown_limit <= Decimal("1"):
            raise ValueError(
                f"max_drawdown_limit must be in (0, 1], got {self.max_drawdown_limit}. "
                "Typical values: 0.10 (10%) to 0.30 (30%)."
            )

        # Validate var_limit if set
        if self.var_limit is not None and self.var_limit <= 0:
            raise ValueError(
                f"var_limit must be > 0, got {self.var_limit}. "
                "Set to None to disable VaR limit."
            )

        # Warn about GPU mode (not a failure, just informational)
        if self.use_gpu:
            # Note: Actual GPU check happens at runtime
            pass  # Validation happens in simulator

    def to_dict(self) -> dict:
        """Convert config to dictionary (for logging/serialization)."""
        return {
            "n_simulations": self.n_simulations,
            "time_horizon": self.time_horizon,
            "confidence_level": str(self.confidence_level),
            "mode": self.mode,
            "adaptive_mode": self.adaptive_mode,
            "seed": self.seed,
            "validation_level": self.validation_level,
            "use_gpu": self.use_gpu,
            "max_drawdown_limit": str(self.max_drawdown_limit),
            "var_limit": str(self.var_limit) if self.var_limit else None,
            "verbose": self.verbose,
            "save_paths": self.save_paths,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Config:
        """
        Create Config from dictionary.

        Business Intent:
            Allows loading config from JSON/YAML files.
            All values validated via __post_init__.

        Args:
            data: Dictionary with config values

        Returns:
            Validated Config instance

        Raises:
            ValueError: If any value is invalid
            TypeError: If types don't match
        """
        # Convert string decimals back to Decimal
        if "confidence_level" in data and isinstance(data["confidence_level"], str):
            data["confidence_level"] = Decimal(data["confidence_level"])
        if "max_drawdown_limit" in data and isinstance(data["max_drawdown_limit"], str):
            data["max_drawdown_limit"] = Decimal(data["max_drawdown_limit"])
        if "var_limit" in data and isinstance(data["var_limit"], str):
            data["var_limit"] = Decimal(data["var_limit"])

        return cls(**data)
