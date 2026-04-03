# Agent Monte Carlo - Production Docker Image
# Multi-stage build for minimal image size

# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==1.7.0

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root --only main

# Stage 2: Runtime image
FROM python:3.11-slim as runtime

WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash agentmc

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/agent-mc /usr/local/bin/agent-mc

# Copy application code
COPY src/agent_mc /app/src/agent_mc
COPY README.md /app/

# Set ownership
RUN chown -R agentmc:agentmc /app

# Switch to non-root user
USER agentmc

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    AGENT_MC_LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from agent_mc import AgentMonteCarloSimulator; print('OK')" || exit 1

# Default command
ENTRYPOINT ["agent-mc"]
CMD ["--help"]

# Metadata
LABEL org.opencontainers.image.title="Agent Monte Carlo"
LABEL org.opencontainers.image.description="Enterprise-grade Monte Carlo simulation framework"
LABEL org.opencontainers.image.version="0.5.0"
LABEL org.opencontainers.image.source="https://github.com/agent-monte-carlo/agent-monte-carlo"
LABEL org.opencontainers.image.licenses="MIT"
