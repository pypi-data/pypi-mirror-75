from fastapi.staticfiles import StaticFiles
from os import path

"""
This serves the /static directory in root folder at /static url.
"""

def install_static(app):
    if path.exists('static'):
        app.mount("/static", StaticFiles(directory="static"), name="static")
