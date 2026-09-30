# 练习44：中间件
# 要求：学习创建中间件、在请求前后执行代码、多个中间件的执行顺序

import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Message, Receive, Scope, Send

app = FastAPI()

# 题目1：基本的中间件 - 添加处理时间头部
# 创建一个FastAPI应用
# 添加中间件，计算每个请求的处理时间
# 将处理时间（秒）添加到响应头部 "X-Process-Time"
# 创建一个路径 /slow/，使用time.sleep(2)模拟慢速操作
# 创建一个路径 /fast/，直接返回{"message": "This is fast"}
# 测试：访问两个路径，检查响应头部中的处理时间

@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start_time:.6f}"
    return response


@app.get("/slow/")
def read_slow() -> dict[str, str]:
    time.sleep(2)
    return {"message": "This is slow"}


@app.get("/fast/")
def read_fast() -> dict[str, str]:
    return {"message": "This is fast"}

# 题目2：中间件修改请求
# 创建中间件，在处理请求前检查自定义头部 "X-Client-ID"
# 如果请求包含这个头部，将其值添加到响应头部 "X-Server-Received-ID"
# 如果不包含，添加响应头部 "X-Server-Received-ID": "unknown"
# 创建路径 /check-client/，返回{"status": "checked"}
# 测试：使用不同请求访问，检查响应头部

@app.middleware("http")
async def read_client_id(request: Request, call_next):
    client_id = request.headers.get("X-Client-ID", "unknown")
    response = await call_next(request)
    response.headers["X-Server-Received-ID"] = client_id
    return response


@app.get("/check-client/")
def check_client() -> dict[str, str]:
    return {"status": "checked"}

# 题目3：中间件修改响应内容
# 创建中间件，为所有响应添加自定义头部 "X-Server-Version" 和 "X-API-Version"
# 值分别为 "1.0.0" 和 "2.0"
# 创建多个路径：GET /users/, GET /items/, POST /data/
# 测试：所有路径的响应都应包含这两个自定义头部

@app.middleware("http")
async def add_version_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Server-Version"] = "1.0.0"
    response.headers["X-API-Version"] = "2.0"
    return response


@app.get("/users/")
def read_users() -> list[dict[str, str]]:
    return [{"username": "alice"}, {"username": "bob"}]


@app.get("/items/")
def read_items() -> list[dict[str, str]]:
    return [{"name": "hammer"}, {"name": "nail"}]


@app.post("/data/")
def write_data(data: dict[str, object]) -> dict[str, int]:
    return {"received_keys": len(data)}

# 题目4：中间件记录请求日志
# 创建中间件，记录每个请求的：
# - HTTP方法
# - URL路径
# - 处理时间
# 打印到控制台，格式："方法 路径 - 处理时间秒"
# 创建路径 /test1/, /test2/, /test3/
# 测试：访问这些路径，检查控制台输出

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    print(f"{request.method} {request.url.path} - {process_time:.6f}")
    return response


@app.get("/test1/")
def read_test1() -> dict[str, str]:
    return {"path": "/test1/"}


@app.get("/test2/")
def read_test2() -> dict[str, str]:
    return {"path": "/test2/"}


@app.get("/test3/")
def read_test3() -> dict[str, str]:
    return {"path": "/test3/"}

# 题目5：多个中间件的执行顺序
# 创建两个中间件：
# 中间件A：在请求前打印"Middleware A - Before"，响应后打印"Middleware A - After"
# 中间件B：在请求前打印"Middleware B - Before"，响应后打印"Middleware B - After"
# 使用@app.middleware("http")装饰器，先定义中间件A，再定义中间件B
# 创建路径 /test-middleware/
# 测试：访问该路径，观察控制台输出的顺序（应该是B-Before, A-Before, A-After, B-After）

@app.middleware("http")
async def middleware_a(request: Request, call_next):
    print("Middleware A - Before")
    response = await call_next(request)
    print("Middleware A - After")
    return response


@app.middleware("http")
async def middleware_b(request: Request, call_next):
    print("Middleware B - Before")
    response = await call_next(request)
    print("Middleware B - After")
    return response


@app.get("/test-middleware/")
def read_test_middleware() -> dict[str, str]:
    return {"middleware": "test"}

# 题目6：中间件过滤特定路径
# 创建中间件，只对路径以"/api/"开头的请求添加响应头部 "X-API-Request": "true"
# 其他路径不添加这个头部
# 创建路径：/api/users/, /api/items/, /public/info/
# 测试：前两个路径应包含头部，第三个不应包含

@app.middleware("http")
async def add_api_request_header(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        response.headers["X-API-Request"] = "true"
    return response


@app.get("/api/users/")
def read_api_users() -> list[dict[str, str]]:
    return [{"username": "alice"}]


@app.get("/api/items/")
def read_api_items() -> list[dict[str, str]]:
    return [{"name": "hammer"}]


@app.get("/public/info/")
def read_public_info() -> dict[str, str]:
    return {"info": "public"}

# 题目7：中间件异常处理
# 创建中间件，捕获路径操作中的异常
# 如果发生异常，返回自定义JSON响应：{"error": "Internal server error", "path": <请求路径>}
# 状态码500
# 创建路径 /error/，故意抛出异常（例如：raise Exception("Test error")）
# 创建路径 /normal/，正常返回数据
# 测试：访问 /error/ 应返回自定义错误响应，访问 /normal/ 应正常返回

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception:
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "path": request.url.path},
            )


app.add_middleware(ExceptionHandlingMiddleware)


@app.get("/error/")
def read_error() -> dict[str, str]:
    raise Exception("Test error")


@app.get("/normal/")
def read_normal() -> dict[str, str]:
    return {"status": "ok"}

# 题目8：综合练习 - 请求ID追踪
# 创建中间件，为每个请求生成唯一ID（使用uuid模块）
# 格式："req-{uuid}"，例如："req-a1b2c3d4"
# 添加到响应头部 "X-Request-ID"
# 在控制台打印：请求ID、方法、路径、处理时间
# 创建多个路径：GET /users/, POST /items/, DELETE /items/{item_id}
# 测试：访问这些路径，每个请求应有唯一ID，控制台应有完整日志

class RequestIDMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request_id = f"req-{uuid.uuid4()}"
        start_time = time.perf_counter()

        async def send_with_request_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                MutableHeaders(scope=message).append("X-Request-ID", request_id)
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        finally:
            process_time = time.perf_counter() - start_time
            print(
                f"{request_id} {scope['method']} {scope['path']} - {process_time:.6f}"
            )


app.add_middleware(RequestIDMiddleware)


@app.get("/users2/")
def read_users2() -> list[dict[str, str]]:
    return [{"username": "alice"}, {"username": "bob"}]


@app.post("/items2/")
def create_item2(item: dict[str, object]) -> dict[str, int]:
    return {"created_keys": len(item)}


@app.delete("/items2/{item_id}")
def delete_item2(item_id: int) -> dict[str, int | str]:
    return {"item_id": item_id, "deleted": "yes"}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
