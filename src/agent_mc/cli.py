#!/usr/bin/env python3
"""
Command-line interface for Agent Monte Carlo.

Business Intent:
    Provides CLI access to simulation functionality.
    Enables scripting, automation, and batch processing.

Design Boundaries:
    - All inputs validated at CLI boundary
    - Fail-fast on invalid arguments
    - Clear error messages with usage hints
    - Structured output (JSON option)

Applicable Scenarios:
    - Running simulations from scripts
    - Batch processing multiple scenarios
    - CI/CD integration
    - Quick testing and validation

Usage:
    agent-mc run --config config.yaml
    agent-mc validate --data data.csv
    agent-mc calibrate --data data.csv --output params.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional


def main(argv: Optional[list[str]] = None) -> int:
    """
    Main CLI entry point.

    Business Intent:
        Parse command-line arguments and dispatch to appropriate command.

    Design Boundaries:
        - Returns 0 on success, non-zero on error
        - Errors printed to stderr
        - Results printed to stdout

    Args:
        argv: Command-line arguments (default: sys.argv[1:])

    Returns:
        Exit code (0 = success, 1 = error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Dispatch to command handler
    if hasattr(args, "func"):
        try:
            return args.func(args)
        except Exception as e:
            # Fail-fast: print error and exit
            print(f"Error: {e}", file=sys.stderr)
            if args.verbose if hasattr(args, "verbose") else False:
                import traceback
                traceback.print_exc()
            return 1
    else:
        parser.print_help()
        return 0


def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser with all subcommands.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="agent-mc",
        description="Agent Monte Carlo - Enterprise-grade simulation framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agent-mc run --config config.yaml
  agent-mc validate --data prices.csv
  agent-mc calibrate --data prices.csv --output params.json
  agent-mc --version
        """,
    )

    # Global options
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.5.0",
        help="Show version and exit",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output",
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run Monte Carlo simulation",
        description="Execute Monte Carlo or ABM simulation with provided config",
    )
    run_parser.add_argument(
        "--config", "-c",
        type=Path,
        required=True,
        help="Path to configuration file (YAML/JSON)",
    )
    run_parser.add_argument(
        "--data", "-d",
        type=Path,
        required=True,
        help="Path to input data file (CSV/Parquet)",
    )
    run_parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output file path (default: stdout)",
    )
    run_parser.add_argument(
        "--format", "-f",
        choices=["json", "csv", "text"],
        default="text",
        help="Output format (default: text)",
    )
    run_parser.set_defaults(func=cmd_run)

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate input data",
        description="Check data quality and format before simulation",
    )
    validate_parser.add_argument(
        "--data", "-d",
        type=Path,
        required=True,
        help="Path to data file to validate",
    )
    validate_parser.add_argument(
        "--schema", "-s",
        type=Path,
        default=None,
        help="Path to schema file (optional)",
    )
    validate_parser.set_defaults(func=cmd_validate)

    # Calibrate command
    calibrate_parser = subparsers.add_parser(
        "calibrate",
        help="Calibrate model parameters",
        description="Automated parameter calibration using Bayesian optimization",
    )
    calibrate_parser.add_argument(
        "--data", "-d",
        type=Path,
        required=True,
        help="Path to historical data",
    )
    calibrate_parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output file for calibrated parameters",
    )
    calibrate_parser.add_argument(
        "--n-trials",
        type=int,
        default=100,
        help="Number of optimization trials (default: 100)",
    )
    calibrate_parser.set_defaults(func=cmd_calibrate)

    return parser


def cmd_run(args: argparse.Namespace) -> int:
    """
    Execute simulation run command.

    Business Intent:
        Load config and data, run simulation, output results.

    Design Boundaries:
        - Validates config file exists
        - Validates data file exists
        - Fails fast on invalid inputs

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 = success)

    Raises:
        FileNotFoundError: If config or data file missing
        ValueError: If config is invalid
    """
    # Validate config file exists
    if not args.config.exists():
        raise FileNotFoundError(f"Config file not found: {args.config}")

    # Validate data file exists
    if not args.data.exists():
        raise FileNotFoundError(f"Data file not found: {args.data}")

    # Placeholder: actual implementation will load config, data, and run simulation
    print(f"Running simulation with config: {args.config}")
    print(f"Loading data from: {args.data}")
    print("Simulation complete (placeholder)")

    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """
    Execute data validation command.

    Business Intent:
        Validate data quality before simulation.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 = valid, 1 = invalid)
    """
    if not args.data.exists():
        raise FileNotFoundError(f"Data file not found: {args.data}")

    print(f"Validating data: {args.data}")
    print("Data validation complete (placeholder)")

    return 0


def cmd_calibrate(args: argparse.Namespace) -> int:
    """
    Execute parameter calibration command.

    Business Intent:
        Calibrate model parameters using historical data.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 = success)
    """
    if not args.data.exists():
        raise FileNotFoundError(f"Data file not found: {args.data}")

    print(f"Calibrating parameters using: {args.data}")
    print(f"Running {args.n_trials} optimization trials")
    print(f"Saving results to: {args.output}")
    print("Calibration complete (placeholder)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
