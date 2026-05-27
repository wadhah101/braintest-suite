#!/usr/bin/env python3
"""
CLI tool to run Braintest test suites: functional tests, eval tests, and load tests.
"""
import sys

import click

from config import load_config

AVAILABLE_SUITES = {
    "functional": "Functional API CRUD tests against Braintrust",
    "evaltest": "Evaluation test with synthetic dataset and scorers",
    "loadtest": "Locust-based load test with concurrent users",
}

CONFIG_KEY_MAP = {
    "functional": "functionaltest",
    "evaltest": "evaltest",
    "loadtest": "loadtest",
}


def _load_config(config_file: str) -> dict:
    try:
        return load_config(config_file)
    except FileNotFoundError:
        click.echo(f"Error: Configuration file not found: {config_file}", err=True)
        sys.exit(1)


def _run_suite(name: str, config: dict) -> str:
    """Run a single test suite by name. Returns status string."""
    if name == "functional":
        click.echo("\n-----Running Functional Test-----")
        from functional_test import run as run_fn

        return "SUCCESS" if run_fn(config) else "FAILED"
    elif name == "evaltest":
        click.echo("\n-----Running Eval Test-----")
        from evaltest import run as run_fn

        return "SUCCESS" if run_fn(config) else "FAILED"
    elif name == "loadtest":
        click.echo("\n-----Running Locust Load Test-----")
        from loadtest import run as run_fn

        return "SUCCESS" if run_fn(config) else "FAILED"
    else:
        return "UNKNOWN"


def _print_results(results: dict):
    click.echo("\n-----Test Summary-----")
    for test_name, status in results.items():
        click.echo(f"{test_name}: {status}")


@click.group(invoke_without_command=True)
@click.option(
    "--config-file",
    default="braintest.yaml",
    show_default=True,
    help="Path to the YAML configuration file.",
)
@click.pass_context
def cli(ctx, config_file):
    """Braintest - test suite runner for Braintrust.

    Run with no arguments to execute all enabled test suites.
    Use 'braintest run <suite> ...' to run specific suites.
    Use 'braintest list' to see available suites.
    """
    ctx.ensure_object(dict)
    ctx.obj["config_file"] = config_file

    if ctx.invoked_subcommand is not None:
        return

    # Default: run all enabled suites
    config = _load_config(config_file)
    results = {}

    click.echo("=" * 50)
    click.echo("Braintest")
    click.echo("=" * 50 + "\n")

    for name in AVAILABLE_SUITES:
        config_key = CONFIG_KEY_MAP[name]
        if config.get(config_key, {}).get("run", False):
            results[name] = _run_suite(name, config)
        else:
            click.echo(f"\n{name} is not enabled in config. Skipping...")
            results[name] = "SKIPPED"

    _print_results(results)

    has_failure = any(s == "FAILED" for s in results.values())
    sys.exit(1 if has_failure else 0)


@cli.command("run")
@click.argument("suites", nargs=-1, required=True)
@click.pass_context
def run_suites(ctx, suites):
    """Run specific test suites by name.

    Examples:

        braintest run functional

        braintest run functional evaltest

        braintest run loadtest
    """
    config_file = ctx.obj["config_file"]

    invalid = [s for s in suites if s not in AVAILABLE_SUITES]
    if invalid:
        click.echo(f"Error: Unknown suite(s): {', '.join(invalid)}", err=True)
        click.echo(f"Available: {', '.join(AVAILABLE_SUITES.keys())}", err=True)
        sys.exit(1)

    config = _load_config(config_file)
    results = {}

    click.echo("=" * 50)
    click.echo("Braintest")
    click.echo("=" * 50 + "\n")

    for name in suites:
        results[name] = _run_suite(name, config)

    _print_results(results)

    has_failure = any(s == "FAILED" for s in results.values())
    sys.exit(1 if has_failure else 0)


@cli.command("list")
def list_suites():
    """List available test suites."""
    click.echo("Available test suites:\n")
    for name, description in AVAILABLE_SUITES.items():
        click.echo(f"  {name:<15} {description}")



if __name__ == "__main__":
    cli()
