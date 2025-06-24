#!/bin/bash

# Go to the directory of this script
cd "$(dirname "$0")"

# Activate the virtual environment
if [ -f "./venv/bin/activate" ]; then
  source ./venv/bin/activate
else
  echo "❌ Could not find ./venv/bin/activate"
  exit 1
fi

# Optional: Set OpenAI API key if .env is present
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
  echo "✅ Environment variables loaded from .env"
fi

# Upgrade pip silently
python3 -m pip install --upgrade pip --quiet

# Start the app
python3 -m prototype.app
