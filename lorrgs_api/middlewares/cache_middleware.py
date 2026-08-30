"""Caching and Timing Middlewares."""

import os
import time

import fastapi
from starlette.datastructures import MutableHeaders


DEFAULT_CACHE_TIMEOUT = os.getenv("DEFAULT_CACHE_TIMEOUT") or 60 * 60  # 1h
DEFAULT_CACHE_HEADER = f"max-age={DEFAULT_CACHE_TIMEOUT}"

# 按路径前缀的缓存策略 (列表顺序 = 匹配优先级):
#   /images        图标基本不变 -> 长缓存, 减少重复请求 (886 个法术图标!)
#   /dist          构建产物, HTML 里带 ?v=<hash> 版本号 -> 可以 immutable 长缓存
#   /data          排名 JSON 由 updater 定期重写 -> no-cache: 浏览器每次带
#                  If-None-Match 回源, 未变化时 StaticFiles 直接回 304, 不重传内容
#   /lorrgs_assets 静态素材 -> 长缓存
#   /api           各路由自带 Cache-Control 的保持不变; 没设置的默认 no-cache,
#                  避免把错误响应缓存一小时
#   / (HTML/JS)    入口页要能立刻看到新版本 -> no-cache
CACHE_POLICY = [
    ("/images", "public, max-age=604800, stale-while-revalidate=86400"),  # 7d
    ("/dist", "public, max-age=31536000, immutable"),  # 1y, ?v= 版本号负责失效
    ("/data", "no-cache"),
    ("/lorrgs_assets", "public, max-age=604800"),  # 7d
    ("/api", "no-cache"),
    ("/", "no-cache"),
]


def get_cache_header(path: str) -> str:
    """Return the Cache-Control value for a request path."""
    for prefix, header in CACHE_POLICY:
        if prefix == "/":
            if path == "/" or path.endswith((".html", ".js")):
                return header
            continue
        if path == prefix or path.startswith(prefix + "/"):
            return header
    return DEFAULT_CACHE_HEADER


class CacheControlMiddleware:
    """纯 ASGI 中间件: 注入默认 Cache-Control + X-Process-Time.

    之前是两个 @app.middleware("http") (BaseHTTPMiddleware), 每个请求都要
    多起一个 anyio task group + 内存流转发 —— 在 t3.small 上一个时间轴页面
    会带来几十个图标请求, 这些开销值得省掉。
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "/")
        start_time = time.perf_counter()

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                process_time = time.perf_counter() - start_time
                headers["X-Process-Time"] = f"{process_time*1000:.04f}ms"
                if "cache-control" not in headers:
                    # 错误响应绝不能长缓存 (否则一个 404 会被浏览器缓存一年)
                    if message.get("status", 200) < 400:
                        headers["Cache-Control"] = get_cache_header(path)
                    else:
                        headers["Cache-Control"] = "no-cache"
            await send(message)

        await self.app(scope, receive, send_with_headers)


def init(app: fastapi.FastAPI, enabled=True):

    if not enabled:
        return

    app.add_middleware(CacheControlMiddleware)
