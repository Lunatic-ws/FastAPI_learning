# 32 简单 OAuth2

## 学习目标

- 理解 OAuth2 密码模式（Password Flow）的完整流程
- 掌握 `OAuth2PasswordBearer` 的使用
- 学会用表单数据接收用户名和密码
- 理解基于依赖注入的用户认证链

## 核心概念

### 1. OAuth2 密码模式流程

1. 前端向登录端点（如 `/token`）发送用户名和密码（表单数据）
2. 后端校验凭据，返回一个 `access_token`（令牌）
3. 前端把令牌存起来，之后每个请求在 `Authorization: Bearer <token>` 头中携带
4. 后端校验令牌，获取当前用户

### 2. 声明 Bearer 令牌方案

`OAuth2PasswordBearer` 本身不校验令牌，只负责提取 `Authorization` 头中的令牌并挂到请求作用域：

```python
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

- `tokenUrl="token"`：告诉文档 UI 客户端令牌端点的地址，供 Swagger UI 自动调用
- 未携带令牌的请求会被自动拒绝，返回 `401` 和 `WWW-Authenticate: Bearer` 头

### 3. 登录端点：接收表单数据

使用 `OAuth2PasswordRequestForm` 接收用户名密码（注意是 `Form` 数据，不是 JSON）：

```python
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Wang",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}

def fake_hash_password(password: str) -> str:
    return "fakehashed" + password

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    return {"access_token": user.username, "token_type": "bearer"}
```

### 4. 获取当前用户（依赖链）

令牌 → 解析出用户 → 过滤掉禁用用户，逐层依赖：

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

def fake_decode_token(token: str) -> UserInDB:
    # 简单示例：直接用 token 当用户名查库
    return UserInDB(**fake_users_db[token])

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
) -> UserInDB:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return current_user

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
):
    return current_user
```

**依赖链结构：**

```
/users/me
  └── get_current_active_user（校验 disabled）
        └── get_current_user（校验令牌有效性）
              └── oauth2_scheme（提取 Bearer 令牌）
```

### 5. 401 响应规范

未认证时返回标准 401：

```python
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="无效的认证凭据",
    headers={"WWW-Authenticate": "Bearer"},
)
```

- `WWW-Authenticate: Bearer` 是 OAuth2 标准要求，客户端据此识别认证方式

## 最佳实践

1. **令牌端点统一叫 `/token`**：与 OAuth2 规范和文档 UI 默认行为一致
2. **依赖分层**：提取令牌、校验用户、校验状态分成独立依赖，各路径按需复用
3. **真实项目**：本页用假哈希和假解码演示流程，真实项目必须配合密码哈希（bcrypt）和 JWT，见下一章
4. **返回 `token_type: "bearer"`**：客户端会拼出 `Bearer <token>` 请求头

## 常见问题

**Q: OAuth2PasswordRequestForm 是 JSON 还是表单？**
A: 是表单数据（`application/x-www-form-urlencoded`），这是 OAuth2 规范要求，用 curl 测试时用 `-d` 而不是 JSON

**Q: Swagger UI 怎么登录？**
A: 右上角 Authorize 按钮，输入用户名密码，它会自动调用 tokenUrl 并在后续请求中带上令牌

**Q: 为什么我拿到的是原始令牌而不是用户对象？**
A: `oauth2_scheme` 只提取令牌字符串，解析用户要在 `get_current_user` 这类依赖里做

## 相关章节

- [28_依赖注入.md](./28_依赖注入.md) - 依赖注入基础
- [29_Security简介.md](./29_Security简介.md) - 安全机制概览
- [30_Security_First_Steps.md](./30_Security_First_Steps.md) - 安全第一步
- [31_Get_Current_User.md](./31_Get_Current_User.md) - 获取当前用户
- [33_带JWT的OAuth2.md](./33_带JWT的OAuth2.md) - 带 JWT 的 OAuth2（真实项目方案）
