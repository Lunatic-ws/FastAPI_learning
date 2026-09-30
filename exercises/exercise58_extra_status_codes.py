# 练习58：额外状态码（Additional Status Codes）
# 本练习文件只有注释，请在下方编写代码实现
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel

app = FastAPI()

"""
任务1: 声明额外状态码
要求:
- 创建Message模型: message(str)
- 创建GET接口 /items/{item_id}
- 使用 responses={404: {"model": Message, "description": "未找到该条目"}} 声明
- item_id不为"foo"时返回数据，否则抛出HTTPException(404)
"""
class Message(BaseModel):
    message: str


@app.get(
    "/items/{item_id}",
    responses={404: {"model": Message, "description": "未找到该条目"}},
    response_model=Message,
)
def read_item(item_id: str) -> Message:
    if item_id == "foo":
        raise HTTPException(status_code=404, detail="未找到该条目")
    return Message(message=f"item {item_id} exists")

"""
任务2: 组合多个额外状态码
要求:
- 创建接口的responses同时声明404和403两种情况
- 403返回模型Message，描述为"权限不足"
- 用查询参数role模拟：role!="admin"时抛出403
"""
@app.get(
    "/admin/items/{item_id}",
    responses={
        403: {"model": Message, "description": "权限不足"},
        404: {"model": Message, "description": "未找到该条目"},
    },
    response_model=Message,
)
def read_admin_item(item_id: str, role: Annotated[str, Query()] = "user") -> Message:
    if role != "admin":
        raise HTTPException(status_code=403, detail="权限不足")
    if item_id == "foo":
        raise HTTPException(status_code=404, detail="未找到该条目")
    return Message(message=f"admin item {item_id}")

"""
任务3: 默认422观察
要求:
- 接收一个int类型参数，传入非法值触发422
- 在 /docs 中观察：422是否自动出现在文档中、额外声明的404/403如何展示
- 在注释中记录：为什么422不需要手动声明
"""
VALIDATION_STATUS_CODE = 422


@app.get("/numbers/{number}")
def read_number(number: int) -> dict[str, int]:
    if number < 0:
        raise HTTPException(status_code=400, detail="number 不能为负数")
    return {"number": number}


@app.get("/numbers-bounded/")
def read_bounded_number(number: Annotated[int, Query(ge=0, le=100)]) -> dict[str, int]:
    return {"number": number}


OPENAPI_RESPONSES = {
    "/items/{item_id}": {"get": [200, 404, 422]},
    "/admin/items/{item_id}": {"get": [200, 403, 404, 422]},
    "/numbers/{number}": {"get": [200, 422]},
    "/numbers-bounded/": {"get": [200, 422]},
    "/items/": {"post": [201, 422]},
    "/items-store/{item_id}": {"get": [200, 404, 422], "delete": [204, 404, 422]},
}


ITEMS = {
    "bar": {"item_id": "bar", "name": "Bar"},
    "baz": {"item_id": "baz", "name": "Baz"},
}


@app.post("/items/", status_code=201, response_model=Message)
def create_item(message: Message) -> Message:
    return message


@app.get(
    "/items-store/{item_id}",
    responses={404: {"model": Message, "description": "未找到该条目"}},
    response_model=Message,
)
def read_stored_item(item_id: str) -> Message:
    item = ITEMS.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="未找到该条目")
    return Message(message=f"item {item_id} exists")


@app.delete(
    "/items-store/{item_id}",
    status_code=204,
    response_class=Response,
    responses={404: {"model": Message, "description": "未找到该条目"}},
)
def delete_stored_item(item_id: str) -> None:
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="未找到该条目")
    ITEMS.pop(item_id)

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)