# 练习41：Get Current User

"""
要求：
1. 创建 User 模型（Pydantic）
2. 实现 fake_decode_token 函数
3. 实现 get_current_user 依赖
4. 创建 /users/me 端点返回当前用户

知识点：
- 用户模型定义
- 依赖注入链（oauth2_scheme -> get_current_user -> User）
- 从 token 解析用户
- 在路径操作中使用用户对象
"""
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

# 题目1：创建用户模型和解析函数
# 实现：
# - User 模型：username (str), email (str|None), full_name (str|None), disabled (bool|None)
# - fake_decode_token(token: str) -> User 函数
#   - 假实现：返回 User(username=token, email="user@example.com", full_name="Test User")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token: str) -> User:
    if not token or not token.replace("-", "").isalnum():
        raise ValueError(f"无法解析的token: {token!r}")
    return User(
        username=token,
        email="user@example.com",
        full_name="Test User",
        disabled=token.startswith("disabled"),
    )

# 题目2：实现 get_current_user 依赖
# 实现：
# - 创建 get_current_user(token: str = Depends(oauth2_scheme)) -> User
# - 调用 fake_decode_token 解析 token
# - 返回 User 对象

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return fake_decode_token(token)

# 题目3：创建用户信息端点
# 实现：
# - GET /users/me 返回当前用户（完整 User 对象）
# - GET /users/me/profile 只返回 username 和 full_name
# - 都需要通过 get_current_user 依赖注入

@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@app.get("/users/me/profile")
def read_users_me_profile(current_user: User = Depends(get_current_user)) -> dict:
    return {"username": current_user.username, "full_name": current_user.full_name}

# 题目4：实现活跃用户检查
# 实现：
# - get_current_active_user 依赖
#   - 依赖 get_current_user
#   - 如果 user.disabled 为 True，抛出 HTTPException(400, detail="Inactive user")
# - GET /active-only 端点使用该依赖
#   - 返回 {"message": "Welcome active user", "username": user.username}

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/active-only")
def read_active_only(user: User = Depends(get_current_active_user)) -> dict:
    return {"message": "Welcome active user", "username": user.username}

# 题目5：错误处理
# 实现：
# - 修改 get_current_user，添加错误处理
# - 如果 token 无效或解析失败，抛出 401 HTTPException
# - 包含 headers={"WWW-Authenticate": "Bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = fake_decode_token(token)
    except ValueError as exc:
        raise credentials_exception from exc
    if user is None:
        raise credentials_exception
    return user


@app.get("/users/me/secured")
def read_users_me_secured(current_user: User = Depends(get_current_user)) -> User:
    return current_user

if __name__ == "__main__":
    pass
