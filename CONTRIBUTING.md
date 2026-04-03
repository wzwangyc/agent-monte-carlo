# Contributing to Agent Monte Carlo

Thank you for your interest in contributing to Agent Monte Carlo! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Commit Guidelines](#commit-guidelines)
- [Security](#security)

---

## Code of Conduct

This project adheres to the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Reporting

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at agent-mc@example.com.

---

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create a branch** for your feature or bugfix
4. **Make your changes** following our coding standards
5. **Submit a Pull Request** for review

---

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Poetry (recommended) or pip
- Git

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/agent-monte-carlo.git
cd agent-monte-carlo

# Install dependencies with Poetry
pip install poetry
poetry install

# Or with pip
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

### Verify Setup

```bash
# Run tests
pytest

# Check code style
ruff check .
black --check .

# Type checking
mypy agent_mc
```

---

## Coding Standards

### General Principles

- **Readability**: Write clear, self-documenting code
- **Maintainability**: Keep functions small and focused
- **Testability**: Write testable code with clear interfaces
- **Performance**: Optimize only after profiling

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting (100 char line length)
- Use [isort](https://pycqa.github.io/isort/) for imports
- Use type hints for all function signatures

### Comments & Documentation

```python
# ✅ Good: Explains WHY, not WHAT
# Using Sobol sequences for better coverage in high-dimensional parameter space
# See: Sobol (1993) "On the distribution of points in a cube"
sobol_sampler = SobolSampler(dim=param_dim)

# ❌ Bad: Just restates the code
# Create a Sobol sampler with the parameter dimension
sobol_sampler = SobolSampler(dim=param_dim)
```

### Financial Logic

- **Never use raw floats** for money, PnL, or returns
- **Always validate inputs** at system boundaries
- **Fail fast**: No silent failures in core logic
- **Explicit units**: Always specify currency, precision, timezone

Example:

```python
from decimal import Decimal
from typing import Literal

class Money:
    """Explicit monetary value with currency and precision."""
    
    def __init__(
        self,
        amount: Decimal,
        currency: Literal["USD", "EUR", "SGD", "CNY"] = "USD"
    ):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.amount = amount
        self.currency = currency
```

---

## Testing

### Test Types

1. **Unit Tests**: Test individual functions/classes
2. **Integration Tests**: Test module interactions
3. **End-to-End Tests**: Test full workflows
4. **Performance Tests**: Benchmark critical paths

### Writing Tests

```python
import pytest
from decimal import Decimal
from agent_mc.core import Money

class TestMoney:
    """Unit tests for Money class."""
    
    def test_positive_amount(self):
        """Valid positive amount should succeed."""
        money = Money(Decimal("100.00"), "USD")
        assert money.amount == Decimal("100.00")
        assert money.currency == "USD"
    
    def test_negative_amount_raises(self):
        """Negative amount should raise ValueError."""
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            Money(Decimal("-100.00"), "USD")
    
    def test_currency_validation(self):
        """Invalid currency should raise ValueError."""
        with pytest.raises(ValueError):
            Money(Decimal("100.00"), "INVALID")
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=agent_mc --cov-report=html

# Specific test file
pytest tests/unit/test_money.py

# Performance benchmarks
pytest benchmarks/ --benchmark-only
```

### Coverage Requirements

- **Core financial logic**: 100% coverage required
- **Risk controls**: 100% coverage required
- **Utility functions**: >80% coverage
- **Overall project**: >70% coverage

---

## Pull Request Process

### Before Submitting

1. **Rebase** onto latest `main` branch
2. **Run all tests** and ensure they pass
3. **Check code style** (ruff, black, mypy)
4. **Update documentation** if needed
5. **Add tests** for new functionality
6. **Update CHANGELOG.md**

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Coverage requirements met

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No new warnings
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least 1 maintainer
3. **Security review** for sensitive changes
4. **Approval** from CODEOWNERS

---

## Commit Guidelines

### Conventional Commits

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Feature
git commit -m "feat(simulator): add adaptive regime switching"

# Bug fix
git commit -m "fix(calibration): correct Sobol index calculation"

# Documentation
git commit -m "docs(readme): add installation instructions"

# Breaking change
git commit -m "feat!: change default confidence level to 0.99"
```

### Sign-off

All commits must be signed off (DCO):

```bash
git commit -s -m "feat: add new feature"
```

This adds: `Signed-off-by: Your Name <your.email@example.com>`

---

## Security

### Reporting Vulnerabilities

**DO NOT** create public issues for security vulnerabilities.

Email: agent-mc@example.com

### Security Guidelines

- Never commit secrets, API keys, or credentials
- Use environment variables for sensitive data
- Validate all external inputs
- Follow fail-fast principles
- Log all sensitive operations

---

## Questions?

- **General questions**: [GitHub Discussions](https://github.com/agent-monte-carlo/agent-monte-carlo/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/agent-monte-carlo/agent-monte-carlo/issues)
- **Security issues**: Email agent-mc@example.com

---

Thank you for contributing to Agent Monte Carlo! 🦁
