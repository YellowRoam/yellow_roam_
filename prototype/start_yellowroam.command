#!/bin/bash
cd "$(dirname "$0")/prototype"
export FLASK_APP=app.py
flask run
