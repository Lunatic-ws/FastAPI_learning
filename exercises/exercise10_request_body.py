# 练习10：请求体
# 要求：使用Pydantic模型和FastAPI实现以下API端点
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# 题目1：创建基本的请求体模型
# 创建User模型：
#   - username: str
#   - email: str
#   - age: int
#   - is_active: bool = True
# POST /users/
# 接收User模型，返回 {"message": "User created", "user": user_dict}
class User(BaseModel):
    username: str
    email: str
    age: int
    is_active: bool = True

@app.post("/users/")
def create_user(user: User):
    return {"message": "User created", "user": user}

# 题目2：可选字段的请求体
# 创建Product模型：
#   - name: str
#   - price: float
#   - description: str | None = None
#   - category: str | None = None
# POST /products/
# 如果description存在，返回包含description的响应
# 否则返回 {"message": "Product created without description"}
class Product(BaseModel):
    name: str
    price: float
    description: str | None = None
    category: str | None = None

@app.post("/products/")
def create_products(product: Product):
    if product.description is not None:
        # return {"name": product.name, "price": product.price, "description": product.description, "category": product.category}
        return product.model_dump()
    return {"message": "Product created without description"}
    
# 题目3：使用模型属性进行计算
# 创建Order模型：
#   - item_name: str
#   - quantity: int
#   - price: float
# POST /orders/
# 计算总价 total = quantity * price
# 返回 {"item": item_name, "quantity": quantity, "total": total}
class Order(BaseModel):
    item_name: str
    quantity: int
    price: float

@app.post("/orders/")
def calculate_orders(order: Order):
    total = order.quantity * order.price
    return {"item": order.item_name, "quantity": order.quantity, "total": total}

# 题目4：请求体 + 路径参数
# 使用题目1的User模型
# PUT /users/{user_id}
# 路径参数：user_id: int
# 请求体：User模型
# 返回 {"user_id": user_id, "updated_user": user_dict}
@app.put("/users/{user_id}")
def put_user(user_id: int, user: User):
    return {"user_id": user_id, "updated_user": user.model_dump()}

# 题目5：请求体 + 路径参数 + 查询参数
# 创建Item模型：
#   - name: str
#   - price: float
# PUT /items/{item_id}
# 路径参数：item_id: int
# 查询参数：discount: float | None = None
# 请求体：Item模型
# 如果discount存在，计算 discounted_price = price * (1 - discount)
# 返回包含item_id、item信息和discounted_price（如果存在）的响应
class Item(BaseModel):
    name: str
    price: float
@app.put("/items/{item_id}")
def put_item(item_id: int, item: Item, discount: float | None = None):
    if discount is not None:
        discounted_price = item.price * (1 - discount)
        return {"item_id": item_id, **item.model_dump(), "discounted_price": discounted_price}
    return {"item_id": item_id, **item.model_dump()}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
