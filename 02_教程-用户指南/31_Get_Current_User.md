# 31 Get Current User

## 学习目标

- 学会从 token 获取当前用户
- 掌握依赖注入链的使用
- 理解用户模型的设计
- 实现假数据认证流程

## 核心概念

### 1. 用户模型

使用 Pydantic 定义用户模型：

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
```

**说明：**
- 可包含任意字段
- 不限于特定数据结构
- 可适配数据库模型

### 2. 解析 Token

创建函数从 token 解析用户：

```python
def fake_decode_token(token: str) -> User:
    # 实际应用中会验证 token 并查询数据库
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe"
    )
```

**注意：** 这是假实现，实际应用需要：
- 验证 token 签名
- 检查过期时间
- 查询用户信息

### 3. get_current_user 依赖

创建获取当前用户的依赖：

```python
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user
```

**依赖链：**
```
请求 -> oauth2_scheme -> token -> get_current_user -> User
```

### 4. 在路径操作中使用

```python
from typing import Annotated

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
```

**优点：**
- 直接获得 User 对象
- 类型提示完整
- 自动认证保护

## 完整示例

```python
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

def fake_decode_token(token: str) -> User:
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
```

## 灵活的数据模型

### 不同的用户模型

```python
# 只包含 id 和 email
class UserMinimal(BaseModel):
    id: int
    email: str

# 数据库模型实例
from sqlalchemy.orm import Session
def get_current_user_db(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return db.query(UserDB).filter(UserDB.token == token).first()
```

### 不同的认证主体

```python
# 机器人/系统认证
class SystemClient(BaseModel):
    client_id: str
    permissions: list[str]

async def get_current_client(token: str = Depends(oauth2_scheme)):
    # 验证系统客户端 token
    return SystemClient(client_id=token, permissions=["read", "write"])
```

## 依赖注入的优势

### 代码复用

```python
# 一次定义，到处使用
@app.get("/profile")
async def get_profile(user: User = Depends(get_current_user)):
    return {"profile": user}

@app.get("/settings")
async def get_settings(user: User = Depends(get_current_user)):
    return {"settings": "user settings"}

@app.delete("/account")
async def delete_account(user: User = Depends(get_current_user)):
    return {"message": "Account deleted"}
```

### 灵活组合

```python
# 不同权限级别
async def get_current_active_user(user: User = Depends(get_current_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

@app.get("/active-only")
async def active_only_endpoint(user: User = Depends(get_current_active_user)):
    return {"message": "Active user only"}
```

## 错误处理

```python
from fastapi import HTTPException, status

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user = fake_decode_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

## 架构设计建议

### 分离关注点

```
auth/
  ├── models.py      # User, Token 等模型
  ├── security.py    # OAuth2 方案, 密码哈希
  ├── dependencies.py # get_current_user 等依赖
  └── routes.py      # /token, /login 等路由
```

### 测试友好

```python
# 依赖可覆盖，便于测试
from fastapi.testclient import TestClient

def test_read_users_me():
    def override_get_current_user():
        return User(username="testuser", email="test@example.com")
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    client = TestClient(app)
    response = client.get("/users/me")
    assert response.status_code == 200
```

## 下一步

- 下一章：Simple OAuth2 - 实现完整的登录端点
- 然后：OAuth2 with JWT - 使用 JWT token

## 参考资源

- [FastAPI Security 文档](https://fastapi.tiangolo.com/tutorial/security/)
- [依赖注入系统](https://fastapi.tiangolo.com/tutorial/dependencies/)
