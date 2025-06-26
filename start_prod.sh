#!/bin/bash
set -e

# Go to the directory of this script
cd "$(dirname "$0")"

# Activate the virtual environment
if [ -f "./venv/bin/activate" ]; then
  echo "Activating virtual environment"
  source ./venv/bin/activate
else
  echo "Could not find ./venv/bin/activate"
  exit 1
fi

# Optional: Set OpenAI API key if .env is present
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
  echo "Environment variables loaded from .env"
fi

# Force upgrade pip to 25.1.1 silently
echo "Upgrading pip to version 25.1.1"
python3 -m pip install --upgrade pip==25.1.1 --quiet

# Start the app with Gunicorn (recommended for production)
echo "Starting Gunicorn server"
exec gunicorn prototype.app:app \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120 \
  --log-level info
