import sqltap
from fastapi import Request, Response
from fastapi.responses import HTMLResponse
import os


"""
This is a SQL logging function.
The SQL report for the last request can be found at:
    /sqltap
This function accumulate data in memory, leading to memory leak.
Don't use it in production by setting ENABLE_SQLTAP=FALSE in env.
"""

statistics = []


def install_sqltap(app):
    enable = os.getenv('ENABLE_SQLTAP', 'false').lower() == 'true'
    if enable:
        @app.middleware("http")
        async def sqltap_logger(request: Request, call_next):
            global statistics
            profiler = sqltap.start()
            response = await call_next(request)
            stat = profiler.collect()
            if len(stat) > 0:
                statistics = stat
            return response

        @app.get('/sqltap', response_class=HTMLResponse, include_in_schema=False)
        def sqltap_view():
            return sqltap.report(statistics,  report_format="html")
