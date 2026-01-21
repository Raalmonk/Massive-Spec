#!/usr/bin/env python
"""Main Entrypoint to create the Backend-APP."""
from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi
from fastapi.middleware.gzip import GZipMiddleware

# IMPORT LOCAL LIBRARIES
from lorgs import data  # pylint: disable=unused-import
from lorrgs_api.middlewares import cache_middleware, cors_middleware
from lorrgs_api.routes import api


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

    app.add_middleware(
        cors_middleware,
        allow_origins=["*"],  # "*" 代表允许任何来源
        allow_credentials=True,
        allow_methods=["*"],  # 允许 GET, POST, OPTIONS 等所有方法
        allow_headers=["*"],  # 允许所有 Header
    )
    
    app.include_router(api.router, prefix="/api")

    cors_middleware.init(app)
    cache_middleware.init(app)
    app.add_middleware(GZipMiddleware, minimum_size=100)

    return app
