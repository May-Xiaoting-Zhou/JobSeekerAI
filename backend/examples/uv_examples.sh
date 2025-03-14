#!/bin/bash

# This script demonstrates common uv commands for managing Python packages

# Make sure we're in the backend directory
cd "$(dirname "$0")/.."

echo "=== UV Examples ==="
echo ""

echo "1. Creating a virtual environment"
echo "Command: uv venv .venv-example"
echo "Description: Creates a new virtual environment in the .venv-example directory"
echo ""

echo "2. Installing a specific package"
echo "Command: uv pip install requests"
echo "Description: Installs the 'requests' package"
echo ""

echo "3. Installing packages from requirements.txt"
echo "Command: uv pip install -r ../requirements.txt"
echo "Description: Installs all packages listed in requirements.txt"
echo ""

echo "4. Installing a specific version of a package"
echo "Command: uv pip install 'fastapi==0.100.0'"
echo "Description: Installs version 0.100.0 of FastAPI"
echo ""

echo "5. Upgrading a package"
echo "Command: uv pip install --upgrade fastapi"
echo "Description: Upgrades FastAPI to the latest version"
echo ""

echo "6. Listing installed packages"
echo "Command: uv pip list"
echo "Description: Lists all installed packages in the current environment"
echo ""

echo "7. Generating a requirements.txt file"
echo "Command: uv pip freeze > requirements.txt"
echo "Description: Creates a requirements.txt file with all installed packages"
echo ""

echo "8. Installing packages in development mode"
echo "Command: uv pip install -e ."
echo "Description: Installs the current package in development mode"
echo ""

echo "9. Uninstalling a package"
echo "Command: uv pip uninstall requests"
echo "Description: Uninstalls the 'requests' package"
echo ""

echo "10. Checking for outdated packages"
echo "Command: uv pip list --outdated"
echo "Description: Lists packages that have newer versions available"
echo ""

echo "These are examples only. Run the actual commands to perform these operations."
echo "For more information, visit: https://github.com/astral-sh/uv"
