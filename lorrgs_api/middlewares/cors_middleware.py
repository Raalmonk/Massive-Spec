"""Adds a CORS Middleware."""
# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
import fastapi
from fastapi.middleware.cors import CORSMiddleware


# TMP FIX
DEBUG = os.getenv("DEBUG")

ORIGINS = [
    "https://lorrgs.io",
    "http://127.0.0.1:5500",  # Live Server Default Port
    "http://localhost:5500",
]
# CloudFlare Pages preview Builds
# (starlette 的 allow_origins 是精确匹配, 通配符需要用 regex)
ORIGIN_REGEX = r"https://.*\.lorrgs-frontend\.pages\.dev"

if DEBUG:
    ORIGINS.append("*")


def init(app: fastapi.FastAPI, enabled=True):

    if not enabled:
        return

    # 注: 之前 ORIGINS 里有 "*" 且 allow_credentials=True, 等于对任意源
    # 开放带凭据的跨域 —— 既是安全问题, 也让浏览器无法复用预检缓存。
    # 前端现在和 API 同源, 只保留白名单即可。
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_origin_regex=ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["*"],
        max_age=3600,
    )
