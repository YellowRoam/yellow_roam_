#!/bin/bash

# ============================================
# 🛠 Local Development Startup Script for Flask
# ============================================

# ✅ Set environment variables 
export SECRET_KEY=6a8d0fb1b24f489b9c8610b7c15aa5fc3c87204f7810d4b6

export FLASK_ENV=development

export OPENAI_API_KEY=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

# ✅ Optional: Activate virtual environment if you use one
# source venv/bin/activate

# ✅ Run the Flask app
echo "🚀 Starting Flask app with development settings..."
python3 prototype/app.py
