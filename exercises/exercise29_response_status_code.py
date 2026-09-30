# 练习29：响应状态码

# 要求：
# 1. 使用 status_code 参数设置不同的HTTP状态码
# 2. 使用 fastapi.status 常量代替魔法数字
# 3. 理解不同操作应返回什么状态码

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()
# 题目1：创建资源API（201 Created）
# POST /products/
# 创建新产品，返回 201 状态码
# 参数：name, price
products: dict[int, dict] = {}

class Product(BaseModel):
    name: str
    price: float

def next_product_id() -> int:
    return max(products, default=0) + 1

@app.post("/products/", status_code=status.HTTP_201_CREATED)
def create_product(product: Product) -> dict:
    item = {
        "id": next_product_id(),
        "name": product.name,
        "price": product.price,
    }
    products[item["id"]] = item
    return item

# 题目2：删除资源API（204 No Content）
# DELETE /products/{product_id}
# 删除产品，返回 204 状态码（无响应体）
# 如果产品不存在，返回 404
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int) -> None:
    if product_id not in products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    del products[product_id]
    return None

# 题目3：获取资源API（200 OK / 404 Not Found）
# GET /products/{product_id}
# 获取产品信息，默认 200
# 如果不存在，抛出 HTTPException 返回 404
@app.get("/products/{product_id}")
def read_product(product_id: int) -> dict:
    if product_id not in products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return products[product_id]

# 题目4：批量操作API
# POST /products/batch
# 批量创建产品，返回 201
# 参数：products 列表
class ProductBatch(BaseModel):
    products: list[Product]

@app.post("/products/batch", status_code=status.HTTP_201_CREATED)
def create_products_batch(batch: ProductBatch) -> list[dict]:
    created: list[dict] = []
    for product in batch.products:
        item = {
            "id": next_product_id(),
            "name": product.name,
            "price": product.price,
        }
        products[item["id"]] = item
        created.append(item)
    return created

# 题目5：更新资源API
# PUT /products/{product_id}
# 更新产品，返回 200
# 如果不存在，返回 404
class ProductUpdate(BaseModel):
    name: str
    price: float

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate) -> dict:
    if product_id not in products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    item = {"id": product_id, "name": product.name, "price": product.price}
    products[product_id] = item
    return item

# 提示：
# - from fastapi import status, HTTPException
# - status.HTTP_201_CREATED
# - status.HTTP_204_NO_CONTENT
# - status.HTTP_404_NOT_FOUND

if __name__ == "__main__":
    pass
