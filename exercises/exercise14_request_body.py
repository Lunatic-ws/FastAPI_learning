# 练习14：请求体
#
# 目标：使用 Pydantic 模型接收和验证 JSON 请求体
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# 任务：
# 1. 创建 Item 模型，包含 name（str）、price（float）、is_offer（bool，可选，默认False）
# 2. 创建 POST /items/ 路由，接收 Item 请求体
# 3. 返回 {"item": item, "message": "Item created successfully"}
# 4. 创建 PUT /items/{item_id} 路由，接收 item_id（int）和 Item 请求体
# 5. 返回 {"item_id": item_id, "item": item, "updated": True}
#
# 提示：
# - 请求体使用 Pydantic BaseModel 声明
# - FastAPI 自动验证 JSON 数据
# - item.dict() 可将模型转为字典
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
def post_item(item: Item):
    return {"item": item.model_dump(), "message": "Item created successfully"}

@app.put("/items/{item_id}")
def put_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item.model_dump(), "updated": True}