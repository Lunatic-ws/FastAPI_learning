# 练习34：错误处理
# 要求：学习使用HTTPException返回错误响应、自定义异常处理器、覆盖默认异常处理器
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from pydantic import BaseModel

app = FastAPI()
# 题目1：基本的HTTPException使用
# 创建一个FastAPI应用，包含一个路径 /items/{item_id}
# 假设有一个字典 items = {"item1": "Laptop", "item2": "Mouse"}
# 当item_id存在时，返回该item
# 当item_id不存在时，抛出HTTPException，状态码404，detail为"Item not found"
# 测试：访问 /items/item1 应返回 {"item": "Laptop"}
# 测试：访问 /items/item3 应返回404错误

items = {"item1": "Laptop", "item2": "Mouse"}


@app.get("/items/{item_id}")
def read_item(item_id: str) -> dict:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

# 题目2：HTTPException带自定义头部
# 创建一个路径 /users/{user_id}
# 假设 user_id 必须是数字字符串，如果是其他值，抛出HTTPException
# 状态码400，detail为"Invalid user ID"，头部添加 {"X-Error-Type": "validation"}
# 测试：访问 /users/abc 应返回400错误，并包含自定义头部

@app.get("/users/{user_id}")
def read_user(user_id: str) -> dict:
    if not user_id.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID",
            headers={"X-Error-Type": "validation"},
        )
    return {"user_id": int(user_id)}

# 题目3：自定义异常和异常处理器
# 定义一个自定义异常类 ItemNotFoundException，接受item_name参数
# 创建一个异常处理器，捕获ItemNotFoundException，返回418状态码（I'm a teapot）
# 响应内容为 {"error": "Item not available", "item": <item_name>}
# 创建路径 /products/{product_name}，当product_name为"discontinued"时抛出ItemNotFoundException
# 测试：访问 /products/discontinued 应返回418状态码

class ItemNotFoundException(Exception):
    def __init__(self, item_name: str) -> None:
        self.item_name = item_name
        super().__init__(f"Item not available: {item_name}")


async def item_not_found_exception_handler(request: Request, exc: ItemNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=418,
        content={"error": "Item not available", "item": exc.item_name},
    )


app.add_exception_handler(ItemNotFoundException, item_not_found_exception_handler)


@app.get("/products/{product_name}")
def read_product(product_name: str) -> dict:
    if product_name == "discontinued":
        raise ItemNotFoundException(product_name)
    return {"product": product_name}

# 题目4：覆盖请求验证异常处理器
# 覆盖RequestValidationError的默认处理器
# 自定义处理器返回纯文本响应，格式为：
# "Validation failed:
# Field: <字段位置>, Message: <错误消息>"
# 对每个验证错误都要换行显示
# 创建路径 /books/{book_id}，book_id类型为int
# 测试：访问 /books/not-a-number 应返回纯文本格式的验证错误

def format_validation_errors(exc: RequestValidationError) -> list[str]:
    lines = ["Validation failed:"]
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"])
        lines.append(f"Field: {location}, Message: {error['msg']}")
    return lines


async def plain_text_validation_handler(request: Request, exc: RequestValidationError) -> PlainTextResponse:
    return PlainTextResponse("\n".join(format_validation_errors(exc)), status_code=422)


app.add_exception_handler(RequestValidationError, plain_text_validation_handler)


@app.get("/books/{book_id}")
def read_book(book_id: int) -> dict:
    return {"book_id": book_id, "title": f"Book {book_id}"}

# 题目5：使用RequestValidationError的body
# 定义Pydantic模型User，包含字段：username (str), age (int)
# 创建POST路径 /users/
# 覆盖RequestValidationError处理器，返回JSON响应包含：
# {"errors": <验证错误列表>, "received_data": <原始请求body>}
# 测试：发送POST请求，body为 {"username": "john", "age": "not-a-number"}
# 应返回包含errors和received_data的JSON

class User(BaseModel):
    username: str
    age: int


async def body_validation_handler(request: Request, exc: RequestValidationError) -> Response:
    raw_body = await request.body()
    if raw_body:
        try:
            received_data = json.loads(raw_body)
        except ValueError:
            received_data = None
        if received_data is not None:
            return JSONResponse(
                status_code=422,
                content={
                    "errors": format_validation_errors(exc),
                    "received_data": received_data,
                },
            )
    return await plain_text_validation_handler(request, exc)


app.add_exception_handler(RequestValidationError, body_validation_handler)


@app.post("/users/")
def create_user(user: User) -> dict:
    return {"username": user.username, "age": user.age}

# 题目6：复用FastAPI默认异常处理器
# 导入fastapi.exception_handlers中的http_exception_handler
# 创建自定义HTTPException处理器，打印错误日志，然后调用默认处理器
# 创建路径 /posts/{post_id}，post_id为int
# 当post_id为0时，抛出HTTPException，状态码404，detail为"Post not found"
# 测试：访问 /posts/0 应在控制台看到日志输出，并返回默认的错误响应格式

async def logging_http_exception_handler(request: Request, exc: HTTPException) -> Response:
    print(f"[error-log] method={request.method} path={request.url.path} status_code={exc.status_code} detail={exc.detail}")
    return await http_exception_handler(request, exc)


app.add_exception_handler(HTTPException, logging_http_exception_handler)


@app.get("/posts/{post_id}")
def read_post(post_id: int) -> dict:
    if post_id == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post_id": post_id, "title": f"Post {post_id}"}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
