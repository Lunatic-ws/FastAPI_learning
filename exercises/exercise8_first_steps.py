# 练习：FastAPI 第一步
#
# 目标：创建最基本的 FastAPI 应用
#
# 任务：
# 1. 导入 FastAPI 并创建 app 实例
# 2. 创建一个 GET / 路由，返回 {"message": "Hello FastAPI"}
# 3. 创建一个 GET /health 路由，返回 {"status": "ok"}
#
# 提示：
# - 使用 @app.get() 装饰器声明路由
# - 函数可以是 async def 或 def
# - return 的字典会自动转为 JSON
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def message():
    return {"message": "Hello FastAPI"}

@app.get("/health")
def health():
    return {"status": "ok"}