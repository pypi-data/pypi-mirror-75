from starlette.middleware.sessions import SessionMiddleware
import os

"""
This is the Starlette official session middleware.
It enable request.session to be used.
e.g.
request.session['id'] = 'abc0001'
id = request.session['id']
"""


def install_session(app):
    secret = os.getenv('FASTAPI_SECRET_KEY', 'gr7a8793hgr832HU2gu')
    app.add_middleware(
        SessionMiddleware,
        secret_key=secret,
        same_site='lax',
        https_only=True
    )
