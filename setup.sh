#!/usr/bin/env bash
set -e  # Exit immediately if a command exits with a non-zero status

VENV_DIR="venv"

# Remove old venv if it exists
if [ -d "$VENV_DIR" ]; then
    echo "Removing existing virtual environment..."
    rm -rf "$VENV_DIR"
fi

# Create new venv
echo "Creating new virtual environment..."
python3 -m venv "$VENV_DIR"

# Activate venv
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping package installation."
fi

echo "Virtual environment setup complete."