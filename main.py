#!/usr/bin/env python3
"""
Main script to orchestrate functionaltest, evaltest, and loadtest execution
based on braintest.yaml config.
"""
import sys

from config import load_config


def main():
    print("="*50)
    print("Braintest")
    print("="*50 + "\n")

    try:
        print("Loading configuration from braintest.yaml...")
        config = load_config()

        results = {}

        if config.get("functionaltest", {}).get("run", False):
            print("\n-----Running Functional Test-----")
            from functional_test import run as run_functionaltest
            success = run_functionaltest(config)
            results["functionaltest"] = (
                "SUCCESS" if success else "FAILED"
            )
        else:
            print("Functional test is not enabled. Skipping...")
            results["functionaltest"] = "SKIPPED"

        if config.get("evaltest", {}).get("run", False):
            print("\n-----Running Eval Test-----")
            from evaltest import run as run_evaltest
            success = run_evaltest(config)
            results["evaltest"] = "SUCCESS" if success else "FAILED"
        else:
            print("\nEvaltest is not enabled. Skipping...")
            results["evaltest"] = "SKIPPED"

        if config.get("loadtest", {}).get("run", False):
            print("\n-----Running Locust Load Test-----")
            from loadtest import run as run_loadtest
            success = run_loadtest(config)
            results["loadtest"] = "SUCCESS" if success else "FAILED"
        else:
            print("\nLoadtest is not enabled. Skipping...")
            results["loadtest"] = "SKIPPED"

        print("\n-----Test Summary-----")
        for test_name, status in results.items():
            print(f"{test_name}: {status}")

    except FileNotFoundError as e:
        print(f"Error: Configuration file not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
