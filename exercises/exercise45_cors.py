# 练习45：CORS跨域资源共享
# 要求：学习配置CORS、理解源的概念、处理跨域请求

import os

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 题目1：基本CORS配置
# 创建FastAPI应用
# 配置CORS中间件，允许以下源：
# - "http://localhost:3000"
# - "http://localhost:8080"
# - "https://example.com"
# 允许所有方法和头部
# 创建路径 GET /api/data/，返回{"data": "This is API data"}
# 提示：使用app.add_middleware(CORSMiddleware, ...)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "https://example.com",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/data/")
def read_api_data() -> dict[str, str]:
    return {"data": "This is API data"}

# 题目2：允许所有源
# 创建FastAPI应用
# 配置CORS中间件，使用allow_origins=["*"]允许所有源
# 允许所有方法和头部
# 创建路径 GET /public/info/，返回{"info": "Public information"}
# 注意：这种方式不支持凭证（cookies、authorization headers等）

app2 = FastAPI()
app2.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app2.get("/public/info/")
def read_public_info() -> dict[str, str]:
    return {"info": "Public information"}

# 题目3：支持凭证的CORS
# 创建FastAPI应用
# 配置CORS中间件：
# - allow_origins：显式指定源列表（不能使用"*"）
# - allow_credentials=True
# - allow_methods：显式指定方法列表（不能使用"*"）
# - allow_headers：显式指定头部列表（不能使用"*"）
# 创建路径 GET /user/profile/，返回{"user": "authenticated user"}
# 提示：当allow_credentials=True时，不能使用通配符

app3 = FastAPI()
app3.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "https://example.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)


@app3.get("/user/profile/")
def read_user_profile() -> dict[str, str]:
    return {"user": "authenticated user"}

# 题目4：限制HTTP方法
# 创建FastAPI应用
# 配置CORS中间件，只允许GET和POST方法
# 允许特定源："http://localhost:3000"
# 创建路径：
# - GET /items/：返回{"items": []}
# - POST /items/：接收JSON数据，返回{"created": true}
# - DELETE /items/{item_id}/：删除项目
# 测试：DELETE请求应被CORS阻止

app4 = FastAPI()
app4.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app4.get("/items/")
def read_items4() -> dict[str, list[str]]:
    return {"items": []}


@app4.post("/items/")
def create_item4(item: dict[str, object]) -> dict[str, bool]:
    return {"created": True}


@app4.delete("/items/{item_id}")
def delete_item4(item_id: int) -> dict[str, int]:
    return {"deleted": item_id}

# 题目5：使用正则表达式匹配源
# 创建FastAPI应用
# 配置CORS中间件，使用allow_origin_regex匹配：
# - 所有https://开头的子域名，如：https://.*\.example\.com
# 允许所有方法和头部
# 创建路径 GET /api/test/，返回{"status": "ok"}
# 提示：allow_origin_regex='https://.*\.example\.com'

app5 = FastAPI()
app5.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.example\.com",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app5.get("/api/test/")
def read_api_test() -> dict[str, str]:
    return {"status": "ok"}

# 题目6：暴露自定义头部
# 创建FastAPI应用
# 配置CORS中间件：
# - 允许源："http://localhost:3000"
# - 使用expose_headers=["X-Custom-Header", "X-Request-ID"]
# 创建路径 GET /custom/，添加两个响应头部：
# - "X-Custom-Header": "custom-value"
# - "X-Request-ID": "12345"
# 返回{"message": "check headers"}
# 提示：使用response.headers["X-Custom-Header"] = "custom-value"

app6 = FastAPI()
app6.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Custom-Header", "X-Request-ID"],
)


@app6.get("/custom/")
def read_custom(response: Response) -> dict[str, str]:
    response.headers["X-Custom-Header"] = "custom-value"
    response.headers["X-Request-ID"] = "12345"
    return {"message": "check headers"}

# 题目7：设置最大缓存时间
# 创建FastAPI应用
# 配置CORS中间件：
# - 允许源："http://localhost:3000"
# - max_age=3600（缓存CORS响应1小时）
# 创建路径 GET /cached/，返回{"cached": "response"}
# 提示：max_age单位是秒

app7 = FastAPI()
app7.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)


@app7.get("/cached/")
def read_cached() -> dict[str, str]:
    return {"cached": "response"}

# 题目8：综合练习 - 完整CORS配置
# 创建FastAPI应用，模拟生产环境配置：
# 配置CORS中间件：
# - 允许的源：从环境变量读取（提供默认值列表）
# - 允许凭证
# - 允许的方法：["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
# - 允许的头部：["*"]
# - 暴露的头部：["X-Total-Count", "X-Page-Count"]
# - 最大缓存时间：86400秒（24小时）
# 创建多个路径操作：
# - GET /api/products/：返回产品列表，添加头部"X-Total-Count"
# - POST /api/products/：创建产品
# - PUT /api/products/{product_id}/：更新产品
# - DELETE /api/products/{product_id}/：删除产品
# 提示：使用import os读取环境变量，os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8080,https://example.com",
).split(",")


class Product(BaseModel):
    id: int = 0
    name: str
    price: float


app8 = FastAPI()
app8.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Page-Count"],
    max_age=86400,
)

products: dict[int, Product] = {
    1: Product(id=1, name="Hammer", price=9.99),
    2: Product(id=2, name="Nail", price=0.5),
}


@app8.get("/api/products/")
def read_products(response: Response) -> list[Product]:
    result = list(products.values())
    response.headers["X-Total-Count"] = str(len(result))
    response.headers["X-Page-Count"] = "1"
    return result


@app8.post("/api/products/")
def create_product(product: Product) -> Product:
    product.id = max(products, default=0) + 1
    products[product.id] = product
    return product


@app8.put("/api/products/{product_id}/")
def update_product(product_id: int, product: Product) -> Product:
    products[product_id] = product.model_copy(update={"id": product_id})
    return products[product_id]


@app8.delete("/api/products/{product_id}/")
def delete_product(product_id: int) -> dict[str, int]:
    products.pop(product_id, None)
    return {"deleted": product_id}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
