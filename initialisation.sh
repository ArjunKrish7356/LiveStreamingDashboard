#!/bin/bash

# Check Python version
required_version=$(cat pythonversion.txt)
current_version=$(python3 --version 2>&1 | awk '{print $2}')
if [[ "$current_version" != "$required_version" ]]; then
    echo "Error: Python version $required_version is required, but $current_version is installed."
    exit 1
fi

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
if [[ "$(uname)" == "Linux" || "$(uname)" == "Darwin" ]]; then
    source .venv/bin/activate
else
    .venv\\Scripts\\activate.bat
fi

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Error: Virtual environment activation failed."
    exit 1
fi

# Install requirements
pip install -r requirements.txt

# Final message
echo "Initialisation complete. When finished, use the 'deactivate' command."
