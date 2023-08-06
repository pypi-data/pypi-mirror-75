from fastapi.middleware.cors import CORSMiddleware
import json
import os

"""
This is the CORS control.
By default, it only allow localhost for dev purpose.
To set other origins, set the CORS_ORIGINS env.
"""


def install_cors(app):
    default = '["http://localhost:8080","http://localhost:8081"]'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', default)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=json.loads(CORS_ORIGINS),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=0
    )
