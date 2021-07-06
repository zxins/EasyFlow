from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from library.exception import ApiException
from services.routers import service_router
from decorators_demo import verify_sign

from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html


def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.48.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.48.0/swagger-ui.css"
    )


# Actual monkey patch
applications.get_swagger_ui_html = swagger_monkey_patch



def init_perm():
    from services.role.entities import MODULES
    print(MODULES)

def create_app():
    app = FastAPI(title="EasyFlow")
    app.include_router(service_router, prefix='/v1')

    # @app.middleware('http')
    # async def verify_sign_middleware(request: Request, call_next):
    #     app_sign: str = request.headers.get('app_sign', '')
    #     app_random: str = request.headers.get('app_random', '')
    #     is_allow = await verify_sign(app_sign, app_random)
    #     if not is_allow:
    #         return JSONResponse(status_code=200, content=dict(code=200003, errMsg="未授权，无法访问", r={}))
    #     response = await call_next(request)
    #     return response


    @app.exception_handler(ApiException)
    async def api_exception(request: Request, exc: ApiException):
        return JSONResponse(status_code=200, content=dict(code=exc.code, errMsg=exc.errMsg, r=exc.r))

    @app.exception_handler(Exception)
    async def unknown_exception(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content=dict(code=1, errMsg="服务器内部错误，暂无法提供服务。", r={}))

    return app

app = create_app()