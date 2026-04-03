# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure setup
- Core configuration module
- CLI entry point
- GitHub Actions CI/CD workflows
- Pre-commit hooks for code quality
- Docker support for containerized deployment

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- Implemented strict input validation at all boundaries
- Added secrets scanning via gitleaks in CI pipeline

---

## [0.5.0] - 2026-04-03

### Added
- Initial release of Agent Monte Carlo framework
- Hybrid MC/ABM simulation engine
- Adaptive regime switching
- Bayesian parameter calibration
- SHAP-based explainability module
- 5-layer validation framework
- GPU acceleration support (CUDA/PyTorch)
- Comprehensive test suite
- Documentation site (Read the Docs)

### Security
- No hardcoded secrets or credentials
- Immutable audit logging
- Strict schema validation
- Fail-fast error handling

---

## Version Numbering

- **Major**: Breaking changes or major architectural shifts
- **Minor**: New features, backward-compatible
- **Patch**: Bug fixes and minor improvements

---

## Release Checklist

For each release, ensure:

- [ ] All tests pass (100% coverage on core modules)
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated
- [ ] Version numbers are consistent across:
  - `pyproject.toml`
  - `README.md`
  - `SECURITY.md`
  - `CHANGELOG.md`
- [ ] Git tag created and pushed
- [ ] GitHub Release published
- [ ] PyPI package uploaded (if applicable)
- [ ] Docker image built and pushed

---

[Unreleased]: https://github.com/agent-monte-carlo/agent-monte-carlo/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/agent-monte-carlo/agent-monte-carlo/releases/tag/v0.5.0
