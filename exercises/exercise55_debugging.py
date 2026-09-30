# 练习55：调试
# 要求：学习如何配置和使用调试器调试FastAPI应用
import asyncio
import logging
import traceback
from collections.abc import Awaitable, Callable, Iterator
from pathlib import Path
from typing import Any, Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d %(message)s",
)
logger = logging.getLogger("exercise55")

app = FastAPI()


def checkpoint(name: str, **values: Any) -> dict[str, Any]:
    caller = traceback.extract_stack()[-2]
    state = {
        "checkpoint": name,
        "location": f"{Path(caller.filename).name}:{caller.lineno}",
        "caller": caller.name,
        "values": {key: repr(value) for key, value in values.items()},
    }
    logger.info("checkpoint %s", state)
    return state


def add_debug_middleware(target: FastAPI) -> None:
    @target.middleware("http")
    async def log_requests(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        body = await request.body()
        logger.info(
            "--> %s %s query=%s body=%s",
            request.method,
            request.url.path,
            dict(request.query_params),
            body.decode("utf-8", errors="replace"),
        )
        response = await call_next(request)
        logger.info(
            "<-- %s %s status=%s content-type=%s",
            request.method,
            request.url.path,
            response.status_code,
            response.headers.get("content-type"),
        )
        return response


# 题目1：创建可调试的FastAPI应用
# 创建一个FastAPI应用，包含以下内容：
# - 在文件中直接调用uvicorn.run()
# - 使用if __name__ == "__main__"保护
# - GET /：返回{"message": "Hello World"}
# - GET /items/{item_id}：返回{"item_id": item_id}
# 在代码中设置断点，使用调试器调试
add_debug_middleware(app)


@app.get("/")
def read_root() -> dict[str, str]:
    checkpoint("root:enter")
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: str) -> dict[str, str]:
    state = checkpoint("items:enter", item_id=item_id, item_id_type=type(item_id).__name__)
    logger.info("items:state=%s", state)
    return {"item_id": item_id}


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")


if __name__ == "__main__":
    main()

# 题目2：调试复杂逻辑
# 创建一个FastAPI应用，包含以下端点：
# - POST /calculate/：接受两个数字a和b
# - 计算a + b, a - b, a * b, a / b
# - 返回所有计算结果
# 在计算过程中设置断点，观察变量值
app2 = FastAPI()
add_debug_middleware(app2)


class CalculateIn(BaseModel):
    a: float
    b: float


class CalculateOut(BaseModel):
    a: float
    b: float
    sum: float
    difference: float
    product: float
    quotient: float


@app2.post("/calculate/")
def calculate(payload: CalculateIn) -> CalculateOut:
    checkpoint("calculate:enter", a=payload.a, b=payload.b)
    total = payload.a + payload.b
    checkpoint("calculate:sum", total=total)
    difference = payload.a - payload.b
    checkpoint("calculate:difference", difference=difference)
    product = payload.a * payload.b
    checkpoint("calculate:product", product=product)
    if payload.b == 0:
        logger.error("calculate: b is zero, cannot divide %s by 0", payload.a)
        raise HTTPException(status_code=400, detail="b 不能为0")
    quotient = payload.a / payload.b
    checkpoint("calculate:quotient", quotient=quotient)
    return CalculateOut(
        a=payload.a,
        b=payload.b,
        sum=total,
        difference=difference,
        product=product,
        quotient=quotient,
    )

# 题目3：调试异步函数
# 创建一个包含异步端点的FastAPI应用：
# - async GET /async-data/：模拟异步操作（使用asyncio.sleep）
# - 返回{"message": "Async data"}
# 在异步函数中设置断点进行调试
app3 = FastAPI()
add_debug_middleware(app3)


async def load_async_data() -> str:
    checkpoint("async:load:start")
    await asyncio.sleep(0.1)
    checkpoint("async:load:after-sleep")
    return "Async data"


@app3.get("/async-data/")
async def read_async_data() -> dict[str, str]:
    checkpoint("async:endpoint:enter")
    message = await load_async_data()
    checkpoint("async:endpoint:exit", message=message)
    return {"message": message}

# 题目4：调试异常处理
# 创建一个FastAPI应用，包含：
# - GET /divide/{a}/{b}：返回a / b的结果
# - 捕获ZeroDivisionError并返回自定义错误
# 在异常处理代码中设置断点
app4 = FastAPI()
add_debug_middleware(app4)


@app4.get("/divide/{a}/{b}")
def divide(a: float, b: float) -> JSONResponse:
    checkpoint("divide:enter", a=a, b=b)
    try:
        result = a / b
    except ZeroDivisionError as error:
        logger.exception("divide: caught %r", error)
        logger.debug("divide: traceback=%s", traceback.format_exc())
        return JSONResponse(
            status_code=400,
            content={
                "error": "ZeroDivisionError",
                "message": "除数不能为0",
                "a": a,
                "b": b,
                "last_frame": traceback.format_exc().splitlines()[-3:-1],
            },
        )
    checkpoint("divide:exit", result=result)
    return JSONResponse(status_code=200, content={"result": result})


@app4.get("/divide-raise/{a}/{b}")
def divide_raise(a: float, b: float) -> dict[str, float]:
    if b == 0:
        logger.error("divide-raise: raising HTTPException(400) for %s / %s", a, b)
        raise HTTPException(status_code=400, detail="除数不能为0")
    return {"result": a / b}

# 题目5：调试依赖注入
# 创建一个包含依赖注入的FastAPI应用：
# - 创建一个依赖函数get_db()
# - GET /users/：使用依赖获取"数据库连接"
# - 返回用户列表
# 在依赖函数和端点中设置断点
app5 = FastAPI()
add_debug_middleware(app5)

USERS = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]


def get_db() -> Iterator[str]:
    connection = "sqlite://:memory:"
    checkpoint("get_db:open", connection=connection)
    try:
        yield connection
    finally:
        checkpoint("get_db:close", connection=connection)


@app5.get("/users/")
def read_users(db: Annotated[str, Depends(get_db)]) -> list[dict[str, Any]]:
    checkpoint("users:enter", db=db, count=len(USERS))
    rows = [{**user, "database": db} for user in USERS]
    checkpoint("users:exit", first=rows[0])
    return rows

# 在下方编写你的代码实现
if __name__ == "__main__":
    # 使用调试器运行此文件
    pass