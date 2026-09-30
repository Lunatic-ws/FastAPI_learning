# 练习63：响应Headers（Response Headers）
# 本练习文件只有注释，请在下方编写代码实现
import time

from fastapi import BackgroundTasks, Depends, FastAPI, Response
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request

app = FastAPI()

"""
任务1: 设置自定义响应头
要求:
- 创建GET接口 /headers/
- 路由函数声明 response: Response 参数
- 设置 response.headers["X-Custom-Header"] = "custom-value"
- 用curl -i观察响应头
"""
@app.get("/headers/")
def get_headers(response: Response):
    response.headers["X-Custom-Header"] = "custom-value"
    return {"message": "已设置自定义响应头"}


"""
任务2: 预先声明响应头（文档可见）
要求:
- 在路径操作装饰器中使用 headers 参数（通过responses或openapi_extra声明）
- 使自定义头出现在 /docs 的响应文档中
- 在注释中说明：只在函数内设置头时为什么文档中看不到
"""
@app.get(
    "/headers/documented/",
    responses={
        200: {
            "headers": {
                "X-Documented-Header": {
                    "description": "在responses中声明的响应头，会出现在/docs中",
                    "schema": {"type": "string"},
                }
            }
        }
    },
)
def get_documented_headers(response: Response):
    response.headers["X-Documented-Header"] = "documented-value"
    return {"message": "响应头已在文档中声明"}


@app.get(
    "/headers/openapi-extra/",
    openapi_extra={
        "responses": {
            200: {
                "headers": {
                    "X-Extra-Header": {
                        "description": "通过openapi_extra声明的响应头",
                        "schema": {"type": "string"},
                    }
                }
            }
        }
    },
)
def get_openapi_extra_headers(response: Response):
    response.headers["X-Extra-Header"] = "extra-value"
    return {"message": "响应头已通过openapi_extra声明"}


"""
任务3: 在依赖中设置响应头
要求:
- 创建依赖函数通过注入的response参数设置 X-Process-Time 头
- 用time.perf_counter()记录处理耗时写入头
- 多个接口复用该依赖
"""
def add_process_time(response: Response):
    started = time.perf_counter()
    elapsed_ms = (time.perf_counter() - started) * 1000
    response.headers["X-Process-Time"] = f"{elapsed_ms:.4f}"


@app.get("/headers/timed/", dependencies=[Depends(add_process_time)])
def get_timed_headers():
    return {"message": "依赖中设置的响应头"}


@app.get("/headers/timed/detail/", dependencies=[Depends(add_process_time)])
def get_timed_headers_detail():
    return {"message": "复用同一个依赖的第二个接口"}


"""
任务4: 返回后才确定值的头
要求:
- 在注释中回答：为什么生成响应后才能设置的值（如Content-Length）
- 需要使用什么机制（提示：与后台任务/中间件结合）
"""
trace_log: list[str] = []


def write_trace_log(message: str) -> None:
    trace_log.append(message)


async def single_chunk(body: bytes):
    yield body


@app.middleware("http")
async def add_content_length(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    response = await call_next(request)
    body = b"".join([chunk async for chunk in response.body_iterator])
    response.body_iterator = single_chunk(body)
    response.headers["X-Content-Length"] = str(len(body))
    return response


@app.get("/headers/late/")
def get_late_headers(task: BackgroundTasks, response: Response):
    task.add_task(write_trace_log, "headers-late")
    response.headers["X-Background-Task"] = "scheduled"
    return {"message": "X-Content-Length由中间件在响应生成后写入"}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
