# 练习38：依赖注入
# 要求：学习创建和使用依赖、共享依赖、层级依赖
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()
# 题目1：基本依赖注入
# 创建依赖函数common_params，接收查询参数：
# - q: str | None = None
# - skip: int = 0
# - limit: int = 100
# 返回字典包含这些参数
# 创建路径 GET /items/ 和 GET /users/
# 使用Depends注入common_params
# 返回注入的依赖结果
# 提示：commons: Annotated[dict, Depends(common_params)]

def common_params(q: str | None = None, skip: int = 0, limit: int = 100) -> dict:
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
def read_items(commons: Annotated[dict, Depends(common_params)]) -> dict:
    return commons


@app.get("/users/")
def read_users(commons: Annotated[dict, Depends(common_params)]) -> dict:
    return commons

# 题目2：共享Annotated依赖
# 创建依赖函数get_pagination，接收page和size参数（默认1和10）
# 创建类型别名PaginationDep = Annotated[dict, Depends(get_pagination)]
# 在多个路径操作中使用这个类型别名：
# - GET /products/
# - GET /orders/
# - GET /customers/
# 所有路径都返回注入的分页参数

def get_pagination(page: int = 1, size: int = 10) -> dict:
    return {"page": page, "size": size, "total_pages": 3}


PaginationDep = Annotated[dict, Depends(get_pagination)]


@app.get("/products/")
def read_products(pagination: PaginationDep) -> dict:
    return {"products": [], "pagination": pagination}


@app.get("/orders/")
def read_orders(pagination: PaginationDep) -> dict:
    return {"orders": [], "pagination": pagination}


@app.get("/customers/")
def read_customers(pagination: PaginationDep) -> dict:
    return {"customers": [], "pagination": pagination}

# 题目3：依赖作为类
# 创建类CommonQueryParams：
# - __init__接收q: str | None = None, skip: int = 0, limit: int = 100
# - 存储为实例属性
# 在路径操作中使用Depends(CommonQueryParams)
# 提示：FastAPI会自动实例化类

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100) -> None:
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/search/")
def search_commons(commons: Annotated[CommonQueryParams, Depends()]) -> dict:
    return {"q": commons.q, "skip": commons.skip, "limit": commons.limit}

# 题目4：依赖返回Pydantic模型
# 创建Pydantic模型User：
# - id: int
# - username: str
# - email: str
# 创建依赖函数get_current_user，返回User实例（模拟认证用户）
# 创建路径 GET /profile/，注入User依赖
# 返回用户信息
# 提示：user: User = Depends(get_current_user)

class User(BaseModel):
    id: int
    username: str
    email: str


def get_current_user() -> User:
    return User(id=1, username="john", email="john@example.com")


@app.get("/profile/")
def read_profile(user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {"user": user}

# 题目5：层级依赖（子依赖）
# 创建依赖函数get_db，返回数据库连接字符串（模拟）
# 创建依赖函数get_user_repo，依赖get_db，返回仓库对象
# 创建依赖函数get_current_user，依赖get_user_repo，返回当前用户
# 创建路径 GET /me/，注入get_current_user依赖
# 返回用户信息
# 提示：层级关系：get_db -> get_user_repo -> get_current_user

def get_db() -> str:
    return "sqlite:///./test.db"


def get_user_repo(db: Annotated[str, Depends(get_db)]) -> dict:
    return {
        "connection": db,
        "users": {
            1: {"id": 1, "username": "john", "email": "john@example.com", "is_admin": True}
        },
    }


def get_current_user2(repo: Annotated[dict, Depends(get_user_repo)]) -> dict:
    return repo["users"][1]


@app.get("/me/")
def read_me(
    user: Annotated[dict, Depends(get_current_user2)],
    repo: Annotated[dict, Depends(get_user_repo)],
) -> dict:
    return {"user": user, "db": repo["connection"]}

# 题目6：依赖中的异常处理
# 创建依赖函数verify_token，接收查询参数token
# 如果token为None或不是"secret"，抛出HTTPException(401, "Invalid token")
# 如果有效，返回{"user_id": 123}
# 创建路径 GET /protected/，注入verify_token依赖
# 返回受保护的数据
# 测试：不带token或错误token应返回401

def verify_token(token: str | None = None) -> dict:
    if token is None or token != "secret":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_id": 123}


@app.get("/protected/")
def read_protected(payload: Annotated[dict, Depends(verify_token)]) -> dict:
    return {"data": "protected resource", "user_id": payload["user_id"]}

# 题目7：全局依赖
# 创建依赖函数require_api_key，检查头部X-API-Key
# 如果不存在或不等于"my-api-key"，抛出HTTPException(403)
# 使用app = FastAPI(dependencies=[Depends(require_api_key)])添加全局依赖
# 创建多个路径操作，所有路径都需要API key
# 提示：所有路径都会自动应用这个依赖

def require_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    if x_api_key != "my-api-key":
        raise HTTPException(status_code=403, detail="Invalid API key")


app.router.dependencies.append(Depends(require_api_key))


@app.get("/api/status/")
def read_status() -> dict:
    return {"status": "ok"}


@app.get("/api/items/")
def read_api_items() -> list[dict]:
    return [{"id": 1, "name": "Hammer"}, {"id": 2, "name": "Nail"}]


@app.post("/api/echo/")
def echo_api_key(x_api_key: Annotated[str | None, Header()] = None) -> dict:
    return {"received": x_api_key is not None}

# 题目8：依赖中的yield（资源清理）
# 创建依赖函数get_db_connection，使用yield返回数据库连接
# 在yield之前：创建连接
# 在yield之后：关闭连接（打印"Connection closed"）
# 创建路径 GET /data/，注入依赖
# 返回{"data": "from database"}
# 提示：使用try/finally确保清理

def get_db_connection() -> Iterator[str]:
    connection = "sqlite:///./yield.db"
    print(f"Connection opened: {connection}")
    try:
        yield connection
    finally:
        print("Connection closed")


@app.get("/data/")
def read_data(connection: Annotated[str, Depends(get_db_connection)]) -> dict:
    return {"data": "from database", "connection": connection}

# 题目9：路径操作装饰器中的依赖
# 创建依赖函数verify_admin，检查用户是否为管理员
# 创建路径 POST /admin/users/，在装饰器中添加依赖：
# @app.post("/admin/users/", dependencies=[Depends(verify_admin)])
# 不在函数参数中注入，只在装饰器中声明
# 返回{"created": true}
# 提示：装饰器中的依赖不返回值，只执行验证

def verify_admin(token: str | None = None) -> None:
    if token != "admin-token":
        raise HTTPException(status_code=403, detail="Admin privileges required")


@app.post("/admin/users/", dependencies=[Depends(verify_admin)])
def create_admin_user() -> dict:
    return {"created": True}

# 题目10：综合练习 - 完整认证系统
# 实现完整的认证依赖层级：
# 1. get_db：数据库连接（yield）
# 2. get_token_from_header：从Authorization头部提取token
# 3. verify_token：验证token有效性（依赖get_token_from_header）
# 4. get_current_user：获取当前用户（依赖verify_token和get_db）
# 5. require_active_user：验证用户是否激活（依赖get_current_user）
# 创建以下路径操作：
# - POST /login/：接收username和password，返回token
# - GET /profile/：需要认证，返回用户信息（依赖get_current_user）
# - GET /admin/：需要管理员权限（依赖require_active_user并检查is_admin）
# - PUT /settings/：需要认证，更新用户设置（依赖get_current_user）
# 提示：使用字典模拟数据库和token存储

class LoginRequest(BaseModel):
    username: str
    password: str


class UserSettings(BaseModel):
    theme: str = "light"
    notifications: bool = True


users_store: dict[int, dict] = {
    1: {
        "id": 1,
        "username": "john",
        "email": "john@example.com",
        "password": "secret",
        "is_admin": True,
        "is_active": True,
    },
    2: {
        "id": 2,
        "username": "jane",
        "email": "jane@example.com",
        "password": "secret",
        "is_admin": False,
        "is_active": True,
    },
    3: {
        "id": 3,
        "username": "bob",
        "email": "bob@example.com",
        "password": "secret",
        "is_admin": False,
        "is_active": False,
    },
}
tokens_store: dict[str, int] = {}


def get_db2() -> Iterator[dict]:
    print("Connection opened: users_store")
    try:
        yield users_store
    finally:
        print("Connection closed")


def get_token_from_header(authorization: Annotated[str | None, Header()] = None) -> str | None:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        return None
    return token or None


def verify_token2(auth: Annotated[dict, Depends(get_token_from_header)]) -> dict:
    if not auth:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if auth not in tokens_store:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_id": tokens_store[auth]}


def get_current_user3(
    token_info: Annotated[dict, Depends(verify_token2)],
    db: Annotated[dict, Depends(get_db2)],
) -> dict:
    user = db.get(token_info["user_id"])
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def require_active_user(user: Annotated[dict, Depends(get_current_user3)]) -> dict:
    if not user.get("is_active"):
        raise HTTPException(status_code=403, detail="Inactive user")
    return user


@app.post("/login/")
def login(login_request: LoginRequest) -> dict:
    for user in users_store.values():
        if user["username"] == login_request.username and user["password"] == login_request.password:
            access_token = f"token-{user['id']}"
            tokens_store[access_token] = user["id"]
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.get("/profile/auth/")
def read_authenticated_profile(user: Annotated[dict, Depends(get_current_user3)]) -> dict:
    return {"id": user["id"], "username": user["username"], "email": user["email"]}


@app.get("/admin/")
def read_admin_panel(user: Annotated[dict, Depends(require_active_user)]) -> dict:
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return {"admin": True, "username": user["username"]}


@app.put("/settings/")
def update_settings(
    settings: UserSettings,
    user: Annotated[dict, Depends(get_current_user3)],
) -> dict:
    user["settings"] = settings.model_dump()
    return {"username": user["username"], "settings": user["settings"]}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
