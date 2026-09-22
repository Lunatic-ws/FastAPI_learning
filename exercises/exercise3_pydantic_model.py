# 练习3：Pydantic模型
# 要求：使用 pydantic 创建数据模型
from pydantic import BaseModel
from typing import Optional
# 题目1：创建Product模型，包含以下字段：
# - name: str
# - price: float
# - quantity: int
# - description: Optional[str] (可选字段)
class Product(BaseModel):
    name: str
    price: float
    quantity: int
    description: Optional[str] = None

# 题目2：创建Order模型，包含以下字段：
# - order_id: str
# - products: list[Product]
# - total_amount: float
class Order(BaseModel):
    order_id: str
    products: list[Product]
    total_amount: float

# 在下方编写你的代码实现
if __name__ == "__main__":
    pass
