# main.py
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

# 1. 将环境变量设置移至全局作用域
# 这样可以确保 uvicorn 在 reload 重新加载模块时，这些变量依然生效，
# 且在 create_app() 执行前就已经就绪。
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

from lorrgs_api.app import create_app  #

# 2. 在这里显式调用工厂函数创建 app 实例
# 这解决了 'Attribute "app" not found' 的错误，因为现在 main 模块里确实有一个全局的 app 变量了。
app = create_app()

if __name__ == "__main__":
    # 3. 启动 uvicorn
    # 注意这里将 import string 改为了 "main:app"
    # "main" 指的是当前文件 (main.py)，"app" 指的是上面创建的全局变量
    #
    # t3.small 调优:
    #   - access_log=False: 每个图标请求一行日志会无限增长 main.log, 请求日志交给 Apache
    #   - proxy_headers + forwarded_allow_ips: 信任本机 Apache 反代的 X-Forwarded-* 头
    #   - limit_concurrency=100: 超载时快速 503, 避免内存被排队请求拖爆
    #   - workers=1: 每个 worker 常驻 ~230MB, 这台机器只有 1.9GB 内存, 不要加
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=5000,
        reload=False,
        workers=1,
        access_log=False,
        log_level="warning",
        proxy_headers=True,
        forwarded_allow_ips="127.0.0.1",
        limit_concurrency=300,
        timeout_keep_alive=5,
    )
