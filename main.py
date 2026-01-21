# main.py
import uvicorn
import os
from lorrgs_api.app import create_app  #

# 1. 将环境变量设置移至全局作用域
# 这样可以确保 uvicorn 在 reload 重新加载模块时，这些变量依然生效，
# 且在 create_app() 执行前就已经就绪。
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

# WCL 客户端 ID 和 Secret
os.environ["WCL_CLIENT_ID"] = "a0e16bba-fba8-432d-a317-4a6a83d98728"
os.environ["WCL_CLIENT_SECRET"] = "Rowpl4stVguifS4YJbzow1HCjh1g2uNuGNaFYRPk"

# 2. 在这里显式调用工厂函数创建 app 实例
# 这解决了 'Attribute "app" not found' 的错误，因为现在 main 模块里确实有一个全局的 app 变量了。
app = create_app()

if __name__ == "__main__":
    # 3. 启动 uvicorn
    # 注意这里将 import string 改为了 "main:app"
    # "main" 指的是当前文件 (main.py)，"app" 指的是上面创建的全局变量
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)