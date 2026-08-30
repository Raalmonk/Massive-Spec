"""GZip middleware that skips already-compressed static assets."""

from starlette.middleware.gzip import GZipMiddleware


class SelectiveGZipMiddleware(GZipMiddleware):
    """starlette 0.32 的 GZipMiddleware 没有 content-type 过滤,
    会把 /images 下 900 多个 PNG 每个请求都重新 gzip 一遍 ——
    压缩率约等于 0, 纯烧 t3.small 的突发 CPU 积分。
    这里按路径前缀跳过图片类挂载点。
    """

    EXCLUDE_PREFIXES = ("/images", "/lorrgs_assets")

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope.get("path", "").startswith(self.EXCLUDE_PREFIXES):
            await self.app(scope, receive, send)
            return
        await super().__call__(scope, receive, send)
