# 练习51：Metadata和文档URLs
# 要求：为FastAPI应用添加元数据和自定义文档URL
from fastapi import FastAPI

# 题目1：创建一个FastAPI应用，包含完整的API元数据
# - 标题："电商平台API"
# - 描述：包含三个部分（产品管理、订单管理、用户管理）的描述（使用Markdown）
# - 摘要："电商平台的RESTful API"
# - 版本："1.0.0"
# - 服务条款URL："https://shop.example.com/terms"
# - 联系信息：name="API支持", email="support@shop.com"
# - 许可证：MIT（使用identifier）
API_DESCRIPTION = """
电商平台 API 提供以下功能：

## 产品管理
查询、创建、更新和删除商品，支持分页与分类筛选。

## 订单管理
创建订单、查询订单状态、取消订单与发起退款。

## 用户管理
用户注册、登录、资料维护与权限管理。
"""

app = FastAPI(
    title="电商平台API",
    description=API_DESCRIPTION,
    summary="电商平台的RESTful API",
    version="1.0.0",
    terms_of_service="https://shop.example.com/terms",
    contact={"name": "API支持", "email": "support@shop.com"},
    license_info={"name": "MIT", "identifier": "MIT"},
)


# 题目2：为应用添加标签元数据
# - "products"标签：描述"产品管理相关操作"
# - "orders"标签：描述"订单处理和管理"，带外部文档链接
# - "users"标签：描述"用户账户管理"
OPENAPI_TAGS = [
    {"name": "products", "description": "产品管理相关操作"},
    {
        "name": "orders",
        "description": "订单处理和管理",
        "externalDocs": {
            "description": "订单接口扩展文档",
            "url": "https://shop.example.com/docs/orders",
        },
    },
    {"name": "users", "description": "用户账户管理"},
]

app.openapi_tags = OPENAPI_TAGS


# 题目3：创建以下路径操作并使用对应标签
# - GET /products：返回产品列表，使用"products"标签
# - GET /orders：返回订单列表，使用"orders"标签
# - GET /users：返回用户列表，使用"users"标签
@app.get("/products", tags=["products"])
def read_products() -> list[dict[str, object]]:
    return [
        {"id": 1, "name": "Hammer", "price": 9.99},
        {"id": 2, "name": "Nail", "price": 0.5},
    ]


@app.get("/orders", tags=["orders"])
def read_orders() -> list[dict[str, object]]:
    return [
        {"id": 1001, "status": "paid", "total_amount": 120.5},
        {"id": 1002, "status": "shipped", "total_amount": 45.0},
    ]


@app.get("/users", tags=["users"])
def read_users() -> list[dict[str, object]]:
    return [
        {"id": 1, "username": "alice", "email": "alice@shop.com"},
        {"id": 2, "username": "bob", "email": "bob@shop.com"},
    ]


# 题目4：配置OpenAPI和文档URLs
# - OpenAPI schema路径："/api/openapi.json"
# - Swagger UI路径："/api/docs"
# - ReDoc路径："/api/redoc"
DEFAULT_DOC_PATHS = {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}

app.router.routes = [
    route for route in app.router.routes if getattr(route, "path", None) not in DEFAULT_DOC_PATHS
]
app.openapi_url = "/api/openapi.json"
app.docs_url = "/api/docs"
app.redoc_url = "/api/redoc"
app.setup()

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
