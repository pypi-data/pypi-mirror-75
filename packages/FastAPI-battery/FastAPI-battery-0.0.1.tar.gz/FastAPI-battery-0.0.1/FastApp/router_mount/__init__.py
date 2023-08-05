from fastapi import Depends, Request
from ..authorization import check_role


"""
This is a helper function replacing include_router.
It is called as:
    app.mount_router(router, tag, roles)
It add the tag and prefix in url, and handle roles check.
"""


def install_router_mount(app):

    def mount(router, tag, roles=None, **options):
        def check_auth(request: Request):
            return check_role(request, roles)

        if roles:
            dependencies = [Depends(check_auth)]
        else:
            dependencies = []

        app.include_router(
            router,
            tags=[tag],
            prefix="/" + tag,
            dependencies=dependencies,
            **options
        )

    app.mount_router = mount
