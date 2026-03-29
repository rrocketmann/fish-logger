#!/bin/bash
# This script sets up the environment and runs the Fish Logger application locally.
# It ensures a clean virtual environment and installs web dependencies.

# Exit immediately if a command exits with a non-zero status.
set -e

VENV_DIR=".venv"

# Create a clean virtual environment
echo "--- Creating a clean virtual environment in $VENV_DIR ---"
rm -rf $VENV_DIR
python3 -m venv $VENV_DIR

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip
echo "--- Upgrading pip ---"
pip install --upgrade pip

# Install web and AI dependencies
echo "--- Installing web application dependencies ---"
pip install -r requirements_web.txt

echo "--- Installing CPU-only AI dependencies ---"
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision
pip install -r requirements_ai.txt

# Run the application
echo "--- Starting the Flask application ---"
export PORT="${PORT:-5001}"
python app/app.py
