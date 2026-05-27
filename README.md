# Braintest Load Test Suite

A load testing suite for running benchmarks on self-hosted Braintrust data planes.

## Overview

This suite currently supports three types of tests:

- **Functional Test** (`functional`): Exercises core API create/read/delete flows across key Braintrust resources
- **Eval Test** (`evaltest`): Generates a large synthetic dataset and runs an eval against it
- **Load Test** (`loadtest`): Spawns simulated users to bombard the data plane with logs, simulating production traffic

The suite can be extended to support additional test types in the future, and that is a goal.

Each test is highly configurable via the `braintest.yaml` config file. The tests should be configured to simulate a customer's expected load and usage patterns. We want to ensure that the infra Braintrust is hosted on can handle the customer's use case, and size up components accordingly if the tests fail.

## Installation

### From source (local development)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone <repo-url> && cd braintest-suite
uv sync
```

### From git (remote install)

```bash
uv pip install git+<repo-url>
```

A default `braintest.yaml` is bundled with the package. If a local `braintest.yaml` exists in the working directory it takes precedence; otherwise the bundled defaults are used.

## Getting Started

1. Create a `.env` file (see `example.env` for reference)

2. Configure `braintest.yaml` with your environment details and test parameters.

3. Run the test suite:
   ```bash
   braintest
   ```

## CLI Usage

The `braintest` CLI is the main entry point. Running it with no arguments executes all suites that are enabled in `braintest.yaml`.

```bash
# Run all enabled test suites (default behavior)
braintest

# List available test suites
braintest list

# Run specific suites (ignores the 'run' flag in config)
braintest run functional
braintest run functional evaltest
braintest run loadtest

# Use a different config file
braintest --config-file custom.yaml
braintest --config-file custom.yaml run loadtest
```

Each test suite is also runnable as a standalone Python module:

```bash
python -m functional_test
python -m evaltest
python -m loadtest
```

If you are running over SSH on a remote server, use `nohup` so the test keeps running if your session disconnects:

```bash
nohup braintest > braintest.out 2>&1 &
```

## Configuration

Configuration is loaded from `braintest.yaml` using [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/). Environment variables take priority over YAML values.

To override any config value via environment variable, use `__` (double underscore) as the nested separator. For example:

| YAML path | Environment variable |
|---|---|
| `braintrust.api_url` | `BRAINTRUST__API_URL` |
| `braintrust.project_name` | `BRAINTRUST__PROJECT_NAME` |
| `loadtest.processes` | `LOADTEST__PROCESSES` |
| `evaltest.trial_count` | `EVALTEST__TRIAL_COUNT` |
| `functionaltest.name_prefix` | `FUNCTIONALTEST__NAME_PREFIX` |

Example:
```bash
BRAINTRUST__API_URL=https://my-api.example.com LOADTEST__PROCESSES=8 uv run braintest
```

## Important Notes
- No actual LLM calls are made in any of these tests. Everything is mocked. The purpose is to load test Braintrust infra, not the LLM provider.
