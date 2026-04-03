## Description

Brief description of changes

Fixes #(issue)

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring (no functional change)

## Testing

- [ ] Tests pass locally (`pytest`)
- [ ] New tests added for new functionality
- [ ] Coverage requirements met (>70% overall, 100% for core financial logic)
- [ ] Manual testing completed (if applicable)

### Test Results
```
Paste test output here
```

## Checklist

- [ ] Code follows project style guidelines (`ruff`, `black`, `isort`)
- [ ] Self-review completed
- [ ] Comments added for complex financial logic
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated
- [ ] No new warnings or errors
- [ ] No hardcoded secrets or credentials
- [ ] All inputs validated at boundaries
- [ ] Fail-fast behavior implemented (if applicable)

## Code Quality

- [ ] Ruff: `ruff check agent_mc tests`
- [ ] Black: `black --check agent_mc tests`
- [ ] mypy: `mypy agent_mc`
- [ ] Bandit: `bandit -r agent_mc`

## Screenshots (if applicable)

Add screenshots to help explain your changes.

## Additional Context

Add any other context about the PR here.

---

**By submitting this PR, I confirm that:**
- I have read and agree to the [Contributing Guide](CONTRIBUTING.md)
- My code follows the [FAST.md](FAST.md) standard
- All financial logic has been audited for correctness
- No sensitive data or secrets are included
