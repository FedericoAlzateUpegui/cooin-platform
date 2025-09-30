#!/usr/bin/env python3
"""
Test runner script for Cooin backend.
Provides different test running options and configurations.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"SUCCESS: {description} completed successfully")
            return True
        else:
            print(f"FAILED: {description} failed with exit code {result.returncode}")
            return False
    except Exception as e:
        print(f"ERROR: Error running {description}: {e}")
        return False


def run_unit_tests():
    """Run unit tests only."""
    command = ["python", "-m", "pytest", "tests/unit/", "-v", "--tb=short"]
    return run_command(command, "Unit Tests")


def run_integration_tests():
    """Run integration tests only."""
    command = ["python", "-m", "pytest", "tests/integration/", "-v", "--tb=short"]
    return run_command(command, "Integration Tests")


def run_all_tests():
    """Run all tests."""
    command = ["python", "-m", "pytest", "tests/", "-v", "--tb=short"]
    return run_command(command, "All Tests")


def run_tests_with_coverage():
    """Run tests with coverage report."""
    command = [
        "python", "-m", "pytest",
        "tests/",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--cov-fail-under=70",
        "-v"
    ]
    return run_command(command, "Tests with Coverage")


def run_specific_test_file(test_file: str):
    """Run specific test file."""
    command = ["python", "-m", "pytest", test_file, "-v", "--tb=short"]
    return run_command(command, f"Specific Test File: {test_file}")


def run_tests_by_marker(marker: str):
    """Run tests with specific marker."""
    command = ["python", "-m", "pytest", f"-m", marker, "-v", "--tb=short"]
    return run_command(command, f"Tests with marker: {marker}")


def run_quick_tests():
    """Run quick tests (exclude slow tests)."""
    command = ["python", "-m", "pytest", "-m", "not slow", "-v", "--tb=short"]
    return run_command(command, "Quick Tests (excluding slow tests)")


def check_test_environment():
    """Check if test environment is properly set up."""
    print("Checking test environment...")

    # Check if pytest is installed
    try:
        import pytest
        print(f"SUCCESS: pytest version: {pytest.__version__}")
    except ImportError:
        print("ERROR: pytest not installed. Run: pip install pytest")
        return False

    # Check if test database can be created
    test_db_path = Path("test.db")
    if test_db_path.exists():
        print("WARNING: Test database exists, will be cleaned up during tests")

    # Check if all test directories exist
    required_dirs = ["tests", "tests/unit", "tests/integration", "tests/fixtures"]
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"SUCCESS: {dir_path}/ directory exists")
        else:
            print(f"ERROR: {dir_path}/ directory missing")
            return False

    # Check key test files
    key_files = [
        "tests/conftest.py",
        "tests/unit/test_auth_service.py",
        "tests/integration/test_auth_api.py",
        "pytest.ini"
    ]
    for file_path in key_files:
        if Path(file_path).exists():
            print(f"SUCCESS: {file_path} exists")
        else:
            print(f"ERROR: {file_path} missing")
            return False

    print("SUCCESS: Test environment is properly configured")
    return True


def clean_test_artifacts():
    """Clean up test artifacts and temporary files."""
    print("Cleaning test artifacts...")

    artifacts_to_clean = [
        "test.db",
        ".pytest_cache",
        "htmlcov",
        "__pycache__",
        ".coverage"
    ]

    for artifact in artifacts_to_clean:
        path = Path(artifact)
        if path.exists():
            if path.is_file():
                path.unlink()
                print(f"Removed file: {artifact}")
            elif path.is_dir():
                import shutil
                shutil.rmtree(path)
                print(f"Removed directory: {artifact}")

    # Clean __pycache__ directories recursively
    for pycache in Path(".").rglob("__pycache__"):
        import shutil
        shutil.rmtree(pycache)
        print(f"Removed: {pycache}")

    print("Test artifacts cleaned")


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Cooin Backend Test Runner")
    parser.add_argument(
        "command",
        choices=[
            "unit", "integration", "all", "coverage", "quick", "check", "clean",
            "auth", "matching", "analytics", "search", "mobile"
        ],
        help="Test command to run"
    )
    parser.add_argument(
        "--file", "-f",
        help="Run specific test file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    print("Cooin Backend Test Runner")
    print("=" * 50)

    success = True

    if args.command == "check":
        success = check_test_environment()
    elif args.command == "clean":
        clean_test_artifacts()
    elif args.command == "unit":
        success = run_unit_tests()
    elif args.command == "integration":
        success = run_integration_tests()
    elif args.command == "all":
        success = run_all_tests()
    elif args.command == "coverage":
        success = run_tests_with_coverage()
    elif args.command == "quick":
        success = run_quick_tests()
    elif args.command in ["auth", "matching", "analytics", "search", "mobile"]:
        success = run_tests_by_marker(args.command)

    if args.file:
        success = run_specific_test_file(args.file)

    # Final summary
    print(f"\n{'='*60}")
    if success:
        print("SUCCESS: Test execution completed successfully!")
        print("All tests passed")

        if args.command == "coverage":
            print("\nCoverage report generated:")
            print("   - Terminal report shown above")
            print("   - HTML report: htmlcov/index.html")

    else:
        print("FAILED: Test execution failed!")
        print("Please check the output above for details")
        sys.exit(1)

    print(f"{'='*60}")


if __name__ == "__main__":
    main()