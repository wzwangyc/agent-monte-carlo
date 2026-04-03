# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.5.x   | :white_check_mark: |
| < 0.5   | :x:                |

## Reporting a Vulnerability

**DO NOT create a public issue for security vulnerabilities.**

### How to Report

Email: **agent-mc@example.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **24 hours**: Initial acknowledgment
- **7 days**: Assessment and fix plan
- **30 days**: Fix released (for critical issues)

### What to Expect

1. **Acknowledgment**: We'll confirm receipt within 24 hours
2. **Assessment**: We'll evaluate severity and impact
3. **Fix Development**: We'll work on a patch
4. **Disclosure**: Coordinated disclosure after fix is available

## Security Best Practices

### For Users

1. **Never commit secrets**
   ```bash
   # Add to .gitignore
   .env
   *.key
   secrets/
   ```

2. **Use environment variables**
   ```python
   import os
   API_KEY = os.environ.get("API_KEY")  # ✅
   API_KEY = "hardcoded-key"  # ❌
   ```

3. **Validate inputs**
   ```python
   from agent_mc.validation import validate_input
   
   data = validate_input(user_input, schema=DataSchema)  # ✅
   data = user_input  # ❌
   ```

4. **Enable audit logging**
   ```python
   from agent_mc.logging import AuditLogger
   
   logger = AuditLogger(enable=True)
   logger.log("trade_executed", trade_id="12345")
   ```

### For Contributors

1. **No hardcoded credentials** in code or tests
2. **No sensitive data** in logs or error messages
3. **Validate all external inputs** at boundaries
4. **Fail fast** on security violations
5. **Use secure defaults** for all configurations

## Security Features

### Input Validation

All external inputs are validated at system boundaries:

```python
from pydantic import BaseModel, validator
from decimal import Decimal

class TradeRequest(BaseModel):
    symbol: str
    quantity: int
    price: Decimal
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v
```

### Audit Logging

All sensitive operations are logged:

- Trade executions
- Configuration changes
- Access control events
- Authentication attempts

Logs are:
- **Immutable**: Cannot be modified after writing
- **Timestamped**: All entries include UTC timestamp
- **Traceable**: Each entry has unique ID

### Secrets Management

- **No secrets in code**: All via environment variables
- **No secrets in logs**: Automatically redacted
- **No secrets in errors**: Generic error messages
- **Encrypted at rest**: Sensitive configs encrypted

### Dependency Security

- **Locked versions**: All dependencies pinned
- **Regular scanning**: Automated vulnerability checks
- **Minimum dependencies**: Only essential packages
- **Verified sources**: Official packages only

## CI/CD Security

### Automated Checks

Every PR triggers:

1. **CodeQL Analysis**: Static security analysis
2. **pip-audit**: Dependency vulnerability scan
3. **gitleaks**: Secrets detection
4. **Bandit**: Python security linter

### Manual Review

- Security-sensitive changes require maintainer approval
- CODEOWNERS review for core modules
- Security team review for critical changes

## Incident Response

### Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| Critical | Active exploitation, data breach | Immediate |
| High | Vulnerability with significant impact | 24 hours |
| Medium | Vulnerability with moderate impact | 7 days |
| Low | Minor security improvement | 30 days |

### Response Process

1. **Detection**: Automated scan or manual report
2. **Triage**: Assess severity and impact
3. **Containment**: Limit damage if active
4. **Eradication**: Fix the vulnerability
5. **Recovery**: Restore normal operations
6. **Lessons Learned**: Document and improve

## Compliance

### Regulatory Alignment

- **Basel III**: Market risk framework
- **SOC 2**: Security controls
- **GDPR**: Data protection (if applicable)
- **PCI DSS**: Payment security (if applicable)

### Audit Trail

All security-relevant events are logged:

- Authentication attempts
- Authorization decisions
- Data access
- Configuration changes
- System events

## Contact

- **Security Email**: agent-mc@example.com
- **PGP Key**: [Available on request]
- **Security Advisories**: [GitHub Security Advisories]

---

**Last Updated**: 2026-04-03
**Version**: 1.0
