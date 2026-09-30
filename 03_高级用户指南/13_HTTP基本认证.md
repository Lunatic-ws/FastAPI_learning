# 13 HTTP基本认证

## 学习目标

- 掌握 `HTTPBasic` 实现浏览器弹窗式认证
- 理解 Basic Auth 的传输方式与安全边界

## 核心概念

### 1. 基本认证流程

HTTP Basic Auth 是最简单的标准认证方式：浏览器弹出用户名/密码输入框，凭据以 `Authorization: Basic <base64(user:password)>` 头随每个请求发送。

### 2. 声明与使用

```python
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

@app.get("/users/me")
async def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}
```

- `HTTPBasicCredentials` 有 `username` 和 `password` 两个属性
- Swagger UI 会显示标准的用户名/密码登录框
- 未认证时 FastAPI 自动返回 `401` 和 `WWW-Authenticate: Basic` 头，浏览器据此弹出输入框

### 3. 校验凭据（防时序攻击）

```python
@app.get("/users/me")
async def read_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username}
```

- **必须用 `secrets.compare_digest`** 而不是 `==`：普通字符串比较是"逐字符短路"的，响应时间差可以被用来逐位猜解凭据（时序攻击）
- 失败时手动抛 401 并带 `WWW-Authenticate: Basic` 头

### 4. 从数据库/环境变量校验

真实项目把用户名密码哈希存库，比对哈希：

```python
correct_hash = get_user_password_hash(credentials.username)
if not verify_password(credentials.password, correct_hash):
    raise HTTPException(status_code=401, headers={"WWW-Authenticate": "Basic"})
```

## 最佳实践

1. **只在 HTTPS 下使用**：Basic Auth 的凭据仅 Base64 编码，明文传输等于裸奔
2. **不用 `==` 比较**：永远用 `secrets.compare_digest` 防时序攻击
3. **适用场景**：内部工具、监控面板、简单管理后台；面向用户的正式产品优先 OAuth2 + JWT
4. **配合中间件**：整个应用都需要认证时，用依赖封装或中间件统一校验

## 常见问题

**Q: 浏览器记住了密码怎么退出？**
A: Basic Auth 无登出机制，浏览器会一直携带凭据，只能关浏览器或清凭据——这也是它不适合 C 端产品的原因之一

**Q: 为什么返回 401 而不是 403？**
A: 401 表示"未认证"（需要提供凭据并触发浏览器弹窗），403 表示"已认证但无权限"

## 相关章节

- [11_高级安全.md](./11_高级安全.md) - 高级安全概览
- [12_OAuth2作用域.md](./12_OAuth2作用域.md) - OAuth2 作用域
- [33_带JWT的OAuth2.md](../02_教程-用户指南/33_带JWT的OAuth2.md) - OAuth2 + JWT
