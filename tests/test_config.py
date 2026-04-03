"""
Unit tests for Config class.

Coverage Requirements:
    - All fields: 100%
    - Validation logic: 100%
    - Edge cases: All boundary conditions
"""

import pytest
from decimal import Decimal

from agent_mc.config import Config


class TestConfig:
    """Unit tests for Config class."""

    def test_default_values(self):
        """Default config should have sensible values."""
        config = Config()
        assert config.n_simulations == 10000
        assert config.time_horizon == 252
        assert config.confidence_level == Decimal("0.95")
        assert config.mode == "hybrid"
        assert config.adaptive_mode is True

    def test_custom_values(self):
        """Custom config should accept provided values."""
        config = Config(
            n_simulations=50000,
            time_horizon=504,
            confidence_level=Decimal("0.99"),
            mode="mc",
            seed=42,
        )
        assert config.n_simulations == 50000
        assert config.time_horizon == 504
        assert config.confidence_level == Decimal("0.99")
        assert config.mode == "mc"
        assert config.seed == 42

    def test_invalid_n_simulations_zero(self):
        """n_simulations=0 should raise ValueError."""
        with pytest.raises(ValueError, match="n_simulations must be > 0"):
            Config(n_simulations=0)

    def test_invalid_n_simulations_negative(self):
        """Negative n_simulations should raise ValueError."""
        with pytest.raises(ValueError, match="n_simulations must be > 0"):
            Config(n_simulations=-1000)

    def test_invalid_time_horizon(self):
        """Negative time_horizon should raise ValueError."""
        with pytest.raises(ValueError, match="time_horizon must be > 0"):
            Config(time_horizon=-252)

    def test_invalid_confidence_too_low(self):
        """Confidence < 0.90 should raise ValueError."""
        with pytest.raises(ValueError, match="confidence_level must be in"):
            Config(confidence_level=Decimal("0.80"))

    def test_invalid_confidence_too_high(self):
        """Confidence > 0.999 should raise ValueError."""
        with pytest.raises(ValueError, match="confidence_level must be in"):
            Config(confidence_level=Decimal("0.9999"))

    def test_invalid_mode(self):
        """Invalid mode should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid mode"):
            Config(mode="invalid")  # type: ignore

    def test_valid_modes(self):
        """All valid modes should be accepted."""
        for mode in ["mc", "abm", "hybrid"]:
            config = Config(mode=mode)  # type: ignore
            assert config.mode == mode

    def test_invalid_max_drawdown(self):
        """Invalid max_drawdown should raise ValueError."""
        with pytest.raises(ValueError, match="max_drawdown_limit must be in"):
            Config(max_drawdown_limit=Decimal("1.5"))

    def test_invalid_var_limit(self):
        """Negative var_limit should raise ValueError."""
        with pytest.raises(ValueError, match="var_limit must be > 0"):
            Config(var_limit=Decimal("-0.05"))

    def test_to_dict(self):
        """Config should serialize to dict."""
        config = Config(n_simulations=20000, seed=123)
        data = config.to_dict()
        assert data["n_simulations"] == 20000
        assert data["seed"] == 123
        assert isinstance(data["confidence_level"], str)

    def test_from_dict(self):
        """Config should deserialize from dict."""
        data = {
            "n_simulations": 20000,
            "time_horizon": 126,
            "confidence_level": "0.99",
            "mode": "abm",
            "seed": 42,
        }
        config = Config.from_dict(data)
        assert config.n_simulations == 20000
        assert config.confidence_level == Decimal("0.99")
        assert config.mode == "abm"
