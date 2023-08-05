from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


"""
This is for error handling.
When any error occur on server, a response is sent to the client:
    {msg, detail, error, source, status_code}
with the corresponding status code.
"""

def install_errata(app):

    @app.exception_handler(IntegrityError)
    async def IntegrityErrorExc(request: Request, e: IntegrityError):
        if 'duplicate' in str(e):
            return handle(e, 'id / unique field duplicated!', str(e), 400)
        elif 'NotNullViolation' in str(e):
            return handle(e, 'Required field cannot be null!', str(e), 400)
        elif 'ForeignKeyViolation' in str(e) and 'update or delete' in str(e):
            return handle(e, 'Foreign key integrity violated!', str(e), 400)
        else:
            return handle(e, 'unknown database integrity error!', str(e), 400)

    @app.exception_handler(NoResultFound)
    async def IntegrityErrorExc(request: Request, e: NoResultFound):
        return handle(e, 'Required item not found!', str(e), 400)

    @app.exception_handler(RequestValidationError)
    async def ValidationExc(request: Request, e: Exception):
        return handle(e, 'Validation Error!', str(e), 422)

    @app.exception_handler(StarletteHTTPException)
    async def HTTPExc(request: Request, e: Exception):
        return handle(e, e.detail, 'HTTP Exception raised', e.status_code)

    @app.exception_handler(AssertionError)
    async def AssertionExc(request: Request, e: AssertionError):
        return handle(e, str(e), str(e), 400)

    @app.exception_handler(Exception)
    async def Exc(request: Request, e: Exception):
        return handle(e, 'Error!', str(e), 400)


def handle(e, msg, detail, status_code):
    content = dict(
        msg=msg,
        detail=detail,
        error=name(e),
        source=fullname(e),
        status_code=status_code
    )
    return JSONResponse(status_code=status_code, content=content)


def fullname(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    else:
        return module + '.' + obj.__class__.__name__


def name(obj):
    return obj.__class__.__name__
