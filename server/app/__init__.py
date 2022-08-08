import time
import os
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import api_router
from setting import settings


def create_application() -> FastAPI:
    # 等待其他组件启动完成
    time.sleep(3)
    app = FastAPI(docs_url='/api/docs')
    app.include_router(api_router, prefix='/api')
    register_middleware(app)
    register_static(app)
    return app


def register_middleware(application):
    if settings.BACKEND_CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def register_static(app):
    # 挂载静态文件
    backend = os.path.dirname(os.path.abspath(__file__))
    app.mount('/static', StaticFiles(directory=os.path.join(backend, 'static')))

    @app.get('/')
    async def read_index():
        return FileResponse(os.path.join(backend, 'static', 'index.html'))

    @app.exception_handler(404)
    async def not_found(request: Request, exc):
        accept = request.headers.get('accept')
        if not accept:
            return JSONResponse(content={'error': "Not found"}, status_code=exc.status_code)
        if exc.status_code == 404 and 'text/html' in accept:
            return FileResponse(os.path.join(backend, 'static', 'index.html'))
        else:
            return JSONResponse(content={'error': "Not found"}, status_code=exc.status_code)