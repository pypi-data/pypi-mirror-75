from .session import login_manager
from .router import router
from fastapi import Request


"""
This is the plugin for SPYC login system.

The SPYC login server should have 2 endpoints:
    -   ENTRY_URL?redirect=
    -   VERIFY_URL?token=

4 routes are opened here:
    -   /login?redirect=
    -   /auth?token=
    -   /logout
    -   /status    # return the whole request.session object

2 helper function is install for setting login manager:

    @app.spyc_login_user_setter
    def func(identity, request: Request):
        # identity is returned by SPYC login server
        # set:
        #   -   request.session['email']             <-- optional 
        #   -   request.session['role']              <-- optional 
        #   -   request.session['login'] : Boolean   <-- compulsory 
        #   -   others...
        Pass

    @app.spyc_login_anonymous_setter
    def func(request: Request):
        # set:
        #   -   request.session['email']             <-- optional 
        #   -   request.session['role']              <-- optional 
        #   -   request.session['login'] : Boolean   <-- compulsory, should be False
        #   -   others...
        Pass

A login check is performed before every request.
If session['login'] == False, then login_manager.set_anonymous is executed.
"""


def install_spyc_login(app):
    app.include_router(router, tags=["login"])

    @app.middleware("http")
    async def set_stranger(request: Request, call_next):
        if not request.session.get('login', False):
            login_manager.set_anonymous(request)
        response = await call_next(request)
        return response

    def user_setter(func):
        login_manager.user_setter(func)

    def anonymous_setter(func):
        login_manager.anonymous_setter(func)

    app.spyc_login_user_setter = user_setter
    app.spyc_login_anonymous_setter = anonymous_setter
