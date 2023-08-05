from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

"""
This is for serving the front-end SPA.

Front-end code should be built into FrontEnd/APP_NAME/dist
The dist folder should have:
    dist/index.html    <-- entry point
    dist/static        <-- all other asset

The front-end will be served at ROOT_URL/APP_NAME
"""


def install_frontend_server(app):
    def serve(name):
        static_folder = f"../FrontEnd/{name}/dist/static"
        index_file = f'../FrontEnd/{name}/dist/index.html'
        static_path = f"/{name.lower()}/static"
        web_path = '/' + name.lower()

        app.mount(static_path, StaticFiles(directory=static_folder), name=f"{name}_static")

        @app.get(web_path + '/{p:path}',  include_in_schema=False)
        def all_paths(p):
            return FileResponse(index_file)

        @app.get(web_path,  include_in_schema=False)
        def root_path():
            return FileResponse(index_file)

    app.serve_frontend = serve
