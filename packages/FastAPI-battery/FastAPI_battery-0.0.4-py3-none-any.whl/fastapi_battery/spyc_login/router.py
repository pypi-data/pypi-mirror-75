import os
import requests
import json
from .session import login_manager
from fastapi import APIRouter, Request, Response, Cookie
from fastapi.responses import RedirectResponse
from typing import Optional

router = APIRouter()


@router.get("/login", include_in_schema=False)
def login(request: Request, redirect: str = None):
    callback = request.url_for("auth")
    url = os.getenv('SPYC_LOGIN_URL_ENTRY') + '?redirect=' + callback
    response = RedirectResponse(url=url)
    if redirect:
        response.set_cookie(key="FASTAPI_REDIRECT", value=redirect)
    return response


@router.get("/auth", include_in_schema=False)
def auth(token: str, request: Request, FASTAPI_REDIRECT: Optional[str] = Cookie(None)):
    identity = verify(token)
    if identity['verified']:
        login_manager.set_user(identity, request)
    else:
        login_manager.set_anonymous(request)
    if FASTAPI_REDIRECT:
        return RedirectResponse(url=FASTAPI_REDIRECT)
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
