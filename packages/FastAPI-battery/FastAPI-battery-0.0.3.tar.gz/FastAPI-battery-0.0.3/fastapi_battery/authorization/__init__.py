from fastapi import HTTPException, Request

"""
This is a helper function to check the role for authorization control in router.

By default, it checks whether session['role'] is in roles.

If not login yet, it raise the 401 error code.
If login in but role unmatched, it raise the 403 error code.

The role_field can be customized to other session properties instead of 'role'.
"""


def check_role(request: Request, roles, role_field='role'):
    login = request.session.get('login', False)
    if not login:
        raise HTTPException(status_code=401, detail="You should login first!")
    role = request.session[role_field]
    if role not in roles:
        raise HTTPException(status_code=403, detail="You have no permission!")
