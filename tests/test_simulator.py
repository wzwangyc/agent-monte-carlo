"""
Unit tests for AgentMonteCarloSimulator.

Coverage Requirements:
    - Input validation: 100%
    - Core simulation: 100%
    - Results calculation: 100%
"""

import pytest
from decimal import Decimal

from agent_mc.config import Config
from agent_mc.simulator import AgentMonteCarloSimulator, SimulationResults


class TestSimulator:
    """Unit tests for AgentMonteCarloSimulator."""

    def test_initialization(self):
        """Simulator should initialize with valid config."""
        config = Config()
        simulator = AgentMonteCarloSimulator(config)
        assert simulator._config == config
        assert simulator._initialized is True

    def test_run_with_valid_data(self):
        """Run should succeed with valid data."""
        config = Config(n_simulations=1000, seed=42)
        simulator = AgentMonteCarloSimulator(config)

        data = {
            "prices": [100.0, 101.5, 99.8, 102.3, 103.1],
        }
        results = simulator.run(data)

        assert isinstance(results, SimulationResults)
        assert results.n_paths == 1000

    def test_run_with_insufficient_data(self):
        """Run should fail with insufficient data."""
        config = Config()
        simulator = AgentMonteCarloSimulator(config)

        data = {
            "prices": [100.0],  # Only 1 price
        }
        with pytest.raises(ValueError, match="Insufficient data"):
            simulator.run(data)

    def test_run_with_missing_prices(self):
        """Run should fail without prices key."""
        config = Config()
        simulator = AgentMonteCarloSimulator(config)

        data = {
            "returns": [0.01, -0.02, 0.03],  # No prices
        }
        with pytest.raises(ValueError, match="must contain 'prices'"):
            simulator.run(data)

    def test_run_with_invalid_data_type(self):
        """Run should fail with non-dict data."""
        config = Config()
        simulator = AgentMonteCarloSimulator(config)

        with pytest.raises(TypeError, match="Data must be dict"):
            simulator.run("invalid")  # type: ignore

    def test_results_structure(self):
        """SimulationResults should have all required fields."""
        results = SimulationResults(
            var_95=Decimal("0.0234"),
            var_99=Decimal("0.0345"),
            es_95=Decimal("0.0289"),
            es_99=Decimal("0.0412"),
            max_drawdown=Decimal("0.1523"),
            mean_return=Decimal("0.0008"),
            std_return=Decimal("0.0156"),
            n_paths=10000,
        )

        assert results.var_95 == Decimal("0.0234")
        assert results.var_99 == Decimal("0.0345")
        assert results.es_95 == Decimal("0.0289")
        assert results.es_99 == Decimal("0.0412")
        assert results.max_drawdown == Decimal("0.1523")
        assert results.mean_return == Decimal("0.0008")
        assert results.std_return == Decimal("0.0156")
        assert results.n_paths == 10000

    def test_results_to_dict(self):
        """Results should serialize to dict."""
        results = SimulationResults(
            var_95=Decimal("0.0234"),
            var_99=Decimal("0.0345"),
            es_95=Decimal("0.0289"),
            es_99=Decimal("0.0412"),
            max_drawdown=Decimal("0.1523"),
            mean_return=Decimal("0.0008"),
            std_return=Decimal("0.0156"),
            n_paths=10000,
        )

        data = results.to_dict()
        assert data["var_95"] == "0.0234"
        assert data["var_99"] == "0.0345"
        assert data["n_paths"] == 10000
