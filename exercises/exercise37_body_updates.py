# 练习37：请求体更新（Body - Updates）
# 要求：根据注释要求实现相应的FastAPI应用
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
# 题目1：PUT整体替换
# 创建Item模型: name(str), description(可选str), price(float), tax(float=10.5)
# 创建内存字典items_db预置1条数据
# 创建PUT接口 /items/{item_id}，直接用新数据整体替换旧数据
# 观察未传的tax字段会被默认值10.5覆盖

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


items_db: dict[str, Item] = {
    "item1": Item(name="Laptop", description="A powerful laptop", price=1000.0, tax=20.0)
}


@app.put("/items/{item_id}")
def replace_item(item_id: str, item: Item) -> Item:
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return items_db[item_id]

# 题目2：PATCH局部更新
# 创建ItemUpdate模型，所有字段均为可选（默认None）
# 创建PATCH接口 /items/{item_id}
# 使用 update_data = body.model_dump(exclude_unset=True) 过滤未设置字段

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | None = None


@app.patch("/items/{item_id}")
def update_item(item_id: str, body: ItemUpdate) -> Item:
    update_data = body.model_dump(exclude_unset=True)
    return merge_item_update(item_id, update_data)

# 题目3：合并更新
# 使用 stored_item_model.model_copy(update=update_data) 生成新对象
# 将合并结果存回items_db，返回更新后的完整数据

def merge_item_update(item_id: str, update_data: dict) -> Item:
    stored_item_model = items_db.get(item_id)
    if stored_item_model is None:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item_model = stored_item_model.model_copy(update=update_data)
    items_db[item_id] = updated_item_model
    return updated_item_model

# 题目4：对比验证
# 分别用PUT和PATCH只更新price字段
# 在注释中回答：tax字段的值在两种方式下分别是什么，为什么

@app.get("/items/{item_id}/update-comparison")
def compare_update_methods(item_id: str) -> dict:
    """
    只提交 price 字段时两种方式的差异:
    - PUT: 请求体整体替换旧数据, 未提供的 tax 取模型默认值 10.5, 原值 20.0 被默认值覆盖;
    - PATCH: model_dump(exclude_unset=True) 过滤掉未提供的 tax, model_copy 只更新 price,
      tax 保持数据库中原有的 20.0。
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    original_item = items_db[item_id]
    put_result = replace_item(item_id, Item(name=original_item.name, price=original_item.price))
    put_tax = put_result.tax
    items_db[item_id] = original_item
    patch_result = update_item(item_id, ItemUpdate(price=original_item.price))
    patch_tax = patch_result.tax
    items_db[item_id] = original_item
    return {
        "item_id": item_id,
        "original_tax": original_item.tax,
        "put_tax": put_tax,
        "patch_tax": patch_tax,
        "explanation": "PUT未传tax时被模型默认值10.5覆盖, PATCH使用exclude_unset过滤未设置字段因此保留原值",
    }

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
