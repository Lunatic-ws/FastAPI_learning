# 33 带JWT的OAuth2

## 学习目标

- 理解 JWT（JSON Web Token）的结构和签名校验原理
- 掌握 PyJWT 签发与解码令牌
- 掌握 passlib + bcrypt 密码哈希
- 完成一个可投入生产的登录认证流程

## 核心概念

### 1. 安装依赖

```bash
pip install "pyjwt[crypto]"
pip install "passlib[bcrypt]"
```

- `pyjwt`：签发和校验 JWT
- `passlib`：处理密码哈希（bcrypt 算法）

### 2. JWT 结构与原理

JWT 由三段 Base64 编码的字符串用 `.` 连接：

```
header.payload.signature
```

- **header**：算法信息（如 `{"alg": "HS256", "typ": "JWT"}`）
- **payload**：数据（claims），如 `{"sub": "alice", "exp": 1727000000}`
- **signature**：用服务端密钥对前两段签名，防止篡改

**关键点**：payload 只是 Base64 编码，任何人都能解码看到内容——JWT 保证的是"内容未被篡改"，不保证"内容保密"。

### 3. 配置与密码哈希

```python
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

- `SECRET_KEY` 生产环境必须用 `openssl rand -hex 32` 生成并放环境变量，不能提交到代码库
- bcrypt 是单向哈希，数据库泄露也无法还原明文密码

### 4. 签发令牌

```python
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

- `sub`（subject）声明用来存用户标识
- `exp`（expiration）声明存过期时间，PyJWT 解码时会自动校验

### 5. 完整登录端点

```python
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
```

### 6. 解码令牌获取当前用户

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user
```

- 令牌过期、签名不对、格式错误都会抛 `InvalidTokenError`，统一转成 401
- 之后的 `get_current_active_user` 依赖链与简单版 OAuth2 完全相同

## 最佳实践

1. **令牌要设过期时间**：永远不要签发永不过期的令牌
2. **`sub` 存用户标识**：解码后据此查库确认用户仍存在且有效
3. **密钥走环境变量**：SECRET_KEY 绝不硬编码
4. **异常细分但不泄露细节**：对外统一"用户名或密码错误"，避免暴露"该用户名存在"
5. **刷新令牌**：短 access token + 长 refresh token 是生产常见做法

## 常见问题

**Q: JWT 和 Session 有什么区别？**
A: JWT 无状态，服务端不用存会话（适合分布式）；Session 有状态但便于主动吊销。JWT 签发后无法直接作废，只能等过期或配合黑名单

**Q: python-jose 和 PyJWT 用哪个？**
A: 官方文档现推荐 PyJWT；老教程多用 python-jose，两者 API 相近（`jwt.encode/decode`）

**Q: passlib 报 bcrypt 版本兼容错误怎么办？**
A: passlib 对新版 bcrypt 有兼容问题，可固定 `bcrypt==4.0.1`，或改用 `bcrypt` 库直接实现哈希

## 相关章节

- [32_简单OAuth2.md](./32_简单OAuth2.md) - 简单 OAuth2（无 JWT 的流程版）
- [28_依赖注入.md](./28_依赖注入.md) - 依赖注入基础
- [04_请求体_已掌握.md](./04_请求体_已掌握.md) - Pydantic 模型基础
