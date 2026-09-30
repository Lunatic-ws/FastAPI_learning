# 练习64：响应更改状态码（Change Status Code）
# 本练习文件只有注释，请在下方编写代码实现

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()

"""
任务1: 默认状态码与声明状态码
要求:
- 创建POST接口 /items/，不声明status_code，观察默认是200
- 创建POST接口 /items2/，声明 status_code=201
- 用curl -i对比两者的响应状态码
"""


class Item(BaseModel):
    name: str
    price: float = 0.0


items_store: dict[str, Item] = {}


@app.post("/items/")
def create_item_default(item: Item) -> Item:
    items_store[item.name] = item
    return item


@app.post("/items2/", status_code=status.HTTP_201_CREATED)
def create_item_declared(item: Item) -> Item:
    items_store[item.name] = item
    return item

"""
任务2: 运行时更改状态码
要求:
- 路由声明 response: Response 参数
- 创建/更新成功时设置 response.status_code = 201
- 资源已存在时设置 response.status_code = 200 并返回已存在数据
- 验证同一接口可返回不同状态码
"""


@app.post("/items/upsert/")
def upsert_item(item: Item, response: Response) -> Item:
    if item.name in items_store:
        response.status_code = status.HTTP_200_OK
        return items_store[item.name]
    items_store[item.name] = item
    response.status_code = status.HTTP_201_CREATED
    return item


@app.get("/items/created/{item_name}", status_code=status.HTTP_201_CREATED)
def item_created(item_name: str, response: Response) -> dict:
    if item_name not in items_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到该条目")
    response.status_code = status.HTTP_200_OK
    return {"name": item_name, "existed": True}

"""
任务3: 文档中的状态码展示
要求:
- 声明status_code=201的接口在/docs中的默认响应如何展示
- 在注释中回答：运行时改状态码会影响文档吗
"""


@app.post(
    "/items3/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_200_OK: {"description": "资源已存在，返回已有数据"}},
)
def create_item_documented(item: Item, response: Response) -> Item:
    if item.name in items_store:
        response.status_code = status.HTTP_200_OK
        return items_store[item.name]
    items_store[item.name] = item
    response.status_code = status.HTTP_201_CREATED
    return item


DOC_TASK3 = {
    "声明status_code=201的接口在/docs中的默认响应如何展示": (
        "201会作为该操作的default响应出现在OpenAPI的responses中，"
        "通过responses={200: {...}}可以额外补充其他状态码的说明。"
    ),
    "运行时改状态码会影响文档吗": (
        "不会。OpenAPI规范在应用启动时由装饰器参数生成，"
        "response.status_code的赋值只作用于本次真实响应，文档里始终显示声明时的状态码。"
    ),
}

"""
任务4: 错误状态码
要求:
- 用HTTPException抛出404，观察其状态码来源
- 在注释中回答：HTTPException的状态码与声明的status_code有什么关系
"""


@app.get("/items-missing/{item_name}")
def read_missing_item(item_name: str) -> Item:
    if item_name not in items_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到该条目",
        )
    return items_store[item_name]


DOC_TASK4 = {
    "HTTPException的状态码与声明的status_code有什么关系": (
        "两者相互独立：装饰器的status_code只决定成功返回时的默认响应码，"
        "HTTPException自带的状态码会覆盖它，且异常响应不会进入文档的default响应中，"
        "需要用responses显式声明才能在/docs看到。"
    ),
}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)