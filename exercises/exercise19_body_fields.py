# 练习19：请求体字段
#
# 目标：使用 Field 为模型属性添加验证
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()
# 任务：
# 1. 创建一个 Item 模型，包含 name（str）、description（可选，最大300字符）、price（必须>0,描述"价格必须大于零"）、tax（可选）
# 2. 使用 Field 添加验证和描述信息
# 3. 创建一个 PUT /items/{item_id} 端点
# 4. 测试发送请求体验证

class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, max_length=300)
    price: float = Field(gt=0, description="价格必须大于零")
    tax: float | None = None
@app.put("/items/{item_id}")
def put_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    return {"item_id": item_id, "item": item}

if __name__ == "__main__":
    pass
