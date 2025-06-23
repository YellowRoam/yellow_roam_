#!/bin/bash
cd "$(dirname "$0")/prototype"

# Optional: activate venv if needed
# source ../.venv/bin/activate

export FLASK_APP=app.py
export FLASK_ENV=development
flask run
