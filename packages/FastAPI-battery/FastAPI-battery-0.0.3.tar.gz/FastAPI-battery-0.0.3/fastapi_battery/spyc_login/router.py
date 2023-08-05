import os
import requests
import json
from .session import login_manager
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/login", include_in_schema=False)
def login(request: Request, redirect: str = None):
    if redirect:
        request.session['FASTAPI_REDIRECT'] = redirect
    callback = request.url_for("auth")
    url = os.getenv('SPYC_LOGIN_URL_ENTRY') + '?redirect=' + callback
    response = RedirectResponse(url=url)
    return response


@router.get("/auth", include_in_schema=False)
def auth(token: str, request: Request):
    identity = verify(token)
    if identity['verified']:
        login_manager.set_user(identity, request)
    else:
        login_manager.set_anonymous(request)
    if 'FASTAPI_REDIRECT' in request.session:
        redirectURL = request.session.pop('FASTAPI_REDIRECT')
        return RedirectResponse(url=redirectURL)
    else:
        return request.session


@router.get("/logout")
def logout(request: Request):
    login_manager.set_anonymous(request)
    return dict(msg='logout success')


@router.get("/status")
def status(request: Request):
    return request.session


def verify(token):
    url = os.getenv('SPYC_LOGIN_URL_VERIFY')
    response = requests.get(url, params={'token': token}).text
    identity = json.loads(response)
    return identity
