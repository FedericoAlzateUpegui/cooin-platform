#!/usr/bin/env python3
"""
Development startup script for Cooin backend.
This script helps you set up and start the development environment.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and return success status."""
    print(f"[RUNNING] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description} completed successfully")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed")
        print(f"   Error: {e.stderr.strip() if e.stderr else e.stdout.strip()}")
        return False

def check_file_exists(filepath, description=""):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"[FOUND] {description} found: {filepath}")
        return True
    else:
        print(f"[NOT FOUND] {description} not found: {filepath}")
        return False

def check_env_file():
    """Check and create .env file if needed."""
    if not Path(".env").exists():
        if Path(".env.example").exists():
            print("[CREATING] Creating .env file from template...")
            try:
                with open(".env.example", "r") as src, open(".env", "w") as dst:
                    content = src.read()
                    # Add some default values for development
                    content = content.replace(
                        "SECRET_KEY=your-super-secret-jwt-key-here-min-32-chars",
                        "SECRET_KEY=dev-secret-key-change-in-production-min32chars"
                    )
                    content = content.replace(
                        "DATABASE_URL=postgresql://username:password@localhost:5432/cooin_db",
                        "DATABASE_URL=postgresql://postgres:password@localhost:5432/cooin_db"
                    )
                    dst.write(content)
                print("[SUCCESS] Created .env file with development defaults")
                print("[WARNING] Remember to update DATABASE_URL with your actual credentials")
                return True
            except Exception as e:
                print(f"[ERROR] Failed to create .env file: {e}")
                return False
        else:
            print("[ERROR] .env.example not found. Cannot create .env file.")
            return False
    else:
        print("[FOUND] .env file already exists")
        return True

def main():
    """Main startup function."""
    print("[COOIN] Cooin Backend Development Setup")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path("app").exists() or not Path("requirements.txt").exists():
        print("[ERROR] This doesn't appear to be the Cooin backend directory")
        print("   Make sure you're in the cooin-backend folder")
        sys.exit(1)

    # Check Python version
    if sys.version_info < (3, 9):
        print("[ERROR] Python 3.9+ is required")
        sys.exit(1)
    print(f"[SUCCESS] Python version: {sys.version.split()[0]}")

    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("[SUCCESS] Virtual environment is active")
    else:
        print("[WARNING] No virtual environment detected. Consider using: python -m venv venv")

    # Check and create .env file
    if not check_env_file():
        print("[WARNING] Please create a .env file before continuing")

    # Check if dependencies are installed
    try:
        import fastapi
        import sqlalchemy
        import alembic
        print("[SUCCESS] Core dependencies are installed")
    except ImportError as e:
        print(f"[ERROR] Missing dependencies. Run: pip install -r requirements.txt")
        if input("Install dependencies now? (y/n): ").lower().startswith('y'):
            if not run_command("pip install -r requirements.txt", "Installing dependencies"):
                sys.exit(1)

    # Check database connection (optional)
    print("\n[CHECKING] Checking database setup...")
    try:
        from app.core.config import settings
        print(f"   Database URL: {settings.DATABASE_URL}")
    except Exception as e:
        print(f"[WARNING] Could not load database configuration: {e}")

    # Run migrations
    print("\n[CHECKING] Checking database migrations...")
    if not run_command("alembic current", "Checking migration status"):
        print("[RUNNING] Running initial migrations...")
        if not run_command("alembic upgrade head", "Running migrations"):
            print("[WARNING] Migration failed. Check your database connection")
            print("   Make sure PostgreSQL is running and the database exists")

    # Offer to start the server
    print("\n" + "=" * 50)
    print("[SUCCESS] Setup complete!")
    print("=" * 50)

    if input("\n[COOIN] Start the development server now? (y/n): ").lower().startswith('y'):
        print("\nStarting FastAPI development server...")
        print("📱 API will be available at: http://localhost:8000")
        print("📚 Interactive docs: http://localhost:8000/api/v1/docs")
        print("[INFO] Press Ctrl+C to stop the server")
        print("\n" + "-" * 50)

        try:
            os.system("uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        except KeyboardInterrupt:
            print("\n👋 Server stopped. See you next time!")

    else:
        print("\n📝 To start manually, run:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        print("\n📚 Then visit: http://localhost:8000/api/v1/docs")

if __name__ == "__main__":
    main()