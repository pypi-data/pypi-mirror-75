from fastapi import FastAPI, Request
from .spyc_login import install_spyc_login
from .sqltap import install_sqltap
from .session import install_session
from .errata import install_errata
from .static import install_static
from .cors import install_cors
from .frontend import install_frontend_server
from .router_mount import install_router_mount


"""
use:
    install_battery(app)
to install all battery.
"""


def install_battery(app):
    install_spyc_login(app)
    install_sqltap(app)  # don't use in production, leak memory
    install_session(app)
    install_errata(app)
    install_static(app)
    install_cors(app)
    install_frontend_server(app)
    install_router_mount(app)

    @app.get("/", include_in_schema=False)
    async def root():
        return 'This is a blank page.'
