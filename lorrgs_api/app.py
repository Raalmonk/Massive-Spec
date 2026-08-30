#!/usr/bin/env python
"""Main Entrypoint to create the Backend-APP."""
from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi
from fastapi.staticfiles import StaticFiles

# IMPORT LOCAL LIBRARIES
from lorgs import data  # pylint: disable=unused-import
from lorrgs_api.middlewares import cache_middleware, cors_middleware
from lorrgs_api.middlewares.gzip_middleware import SelectiveGZipMiddleware
from lorrgs_api.routes import api
from lorrgs_api.routes import views

def create_app() -> fastapi.FastAPI:
    """Create and return a new QuartApp-Instance.

    Returns:
        <Quart>: the new Quart-app instance

    """

    # Quart
    app = fastapi.FastAPI(
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",  # must be in "/api" so the AppEngine route works
    )

    app.include_router(api.router, prefix="/api")
    app.include_router(views.router)

    app.mount("/images", StaticFiles(directory="front_end/images"), name="images")

    # 同样挂载数据文件夹
    app.mount("/data", StaticFiles(directory="front_end/data"), name="data")

    # 预编译的前端资源 (scripts/build_frontend.py 的产物: app.js / app.css)
    app.mount("/dist", StaticFiles(directory="front_end/dist"), name="dist")

    app.mount("/lorrgs_assets", StaticFiles(directory="lorrgs_assets"), name="assets")

    cors_middleware.init(app)
    cache_middleware.init(app)
    # compresslevel=6: 默认的 9 在 t3.small 突发实例上白烧 CPU，压缩率几乎没差别;
    # SelectiveGZip 跳过 /images 等已压缩资源 (PNG 再 gzip 没有收益)
    app.add_middleware(SelectiveGZipMiddleware, minimum_size=500, compresslevel=6)

    return app
