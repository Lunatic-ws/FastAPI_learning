# 练习18: 多请求体参数
# 要求：根据注释要求实现相应的FastAPI应用
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
# 题目1: 混合参数类型
# 创建一个PUT接口 /items/{item_id}
# 路径参数 item_id: 整数，范围0-1000
# 查询参数 q: 可选字符串
# 请求体 item: Item模型，可选
# Item模型包含: name(str), description(可选str), price(float), tax(可选float)
# 返回包含item_id的字典，如果q存在则添加，如果item存在则添加
class Item1(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
def put_itemid(
        item_id: Annotated[int, Path(ge = 0, le = 1000)],
        q: str | None =None,
        item: Item1 | None = None
):
    results = {"item_id": item_id}

    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# 题目2: 多个请求体参数
# 创建一个PUT接口 /update/{item_id}
# 路径参数 item_id: 整数
# 请求体参数 item: Item模型
# 请求体参数 user: User模型
# Item模型: name(str), price(float)
# User模型: username(str), full_name(可选str)
# 返回包含item_id, item, user的字典
# 注意：请求体JSON应该包含"item"和"user"两个键
class Item(BaseModel):
    name: str
    price: float

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/update/{item_id}")
def put_item_id(
    item_id: int,
    item: Item,
    user: User
):
    return {"item_id": item_id, "item": item, "user": user}

# 题目3: 请求体中的单一值
# 创建一个PUT接口 /process/{item_id}
# 路径参数 item_id: 整数
# 请求体参数 item: Item模型
# 请求体参数 user: User模型
# 请求体参数 importance: 整数（使用Body()声明）
# Item模型: name(str), price(float)
# User模型: username(str), full_name(可选str)
# 返回包含所有参数的字典
# importance应该大于0（使用Body(gt=0)）
@app.put("/process/{item_id}")
def put_process(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)]
):
    return {"item_id": item_id, "item": item, "user": user, "importance": importance}

# 题目4: 嵌入单个请求体参数
# 创建一个PUT接口 /items/{item_id}/embed
# 路径参数 item_id: 整数
# 请求体参数 item: Item模型（使用Body(embed=True)）
# Item模型: name(str), price(float)
# 返回包含item_id和item的字典
# 注意：请求体JSON应该是{"item": {"name": "...", "price": ...}}
@app.put("/items/{item_id}/embed")
def put_item_embed(
    item_id: int,
    item: Annotated[Item, Body(embed=True)],
):
    return {"item_id": item_id, "item": item}

# 题目5: 综合应用
# 创建一个POST接口 /complex-operation
# 查询参数 operation: 字符串，可选
# 请求体参数 source: Source模型
# 请求体参数 target: Target模型
# 请求体参数 priority: 整数（使用Body()）
# Source模型: id(int), name(str)
# Target模型: id(int), name(str)
# priority应该大于0且小于10
# 返回包含operation(如果存在), source, target, priority的字典
class Source(BaseModel):
    id: int
    name: str

class Target(BaseModel):
    id: int
    name: str

@app.post("/complex-operation")
def post_operation(
    source: Source,
    target: Target,
    priority: Annotated[int, Body(gt=0, lt=10)],
    operation: Annotated[str | None, Query()] = None  # 查询参数
):
    if operation is not None:
        return {"operation": operation, "source": source, "target": target, "priority": priority}
    return {"source": source, "target": target, "priority": priority}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
