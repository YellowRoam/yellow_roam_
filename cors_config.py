# cors_config.py
from flask_cors import CORS

def configure_cors(app):
    CORS(
        app,Add commentMore actions
        resources={r"/api/*": {"origins": "https://yellowroam.github.io"}},
        supports_credentials=True
    )
