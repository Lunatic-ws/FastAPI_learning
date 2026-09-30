# 30 Security - First Steps

## 学习目标

- 理解 OAuth2 password flow
- 掌握 OAuth2PasswordBearer 使用
- 理解 token 认证流程
- 学会在 FastAPI 中集成安全工具

## 核心概念

### 1. OAuth2 Password Flow

OAuth2 定义了多种认证流程（flows），`password` flow 适合同一应用的前后端认证：

**流程步骤：**
1. 用户在前端输入 `username` 和 `password`
2. 前端发送到指定 `tokenUrl`（如 `/token`）
3. 后端验证并返回 `access_token`
4. 前端存储 token，后续请求携带 `Authorization: Bearer <token>`
5. 后端验证 token 是否有效

**特点：**
- Token 通常有过期时间
- Token 被盗风险相对较低（非永久密钥）
- 适合同应用场景

### 2. OAuth2PasswordBearer

FastAPI 提供 `OAuth2PasswordBearer` 类实现 Bearer Token 认证：

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

**参数说明：**
- `tokenUrl`：客户端发送 username/password 获取 token 的 URL
- 相对 URL，会基于当前 API 地址计算完整路径

**注意：**
- `tokenUrl="token"` 不创建该路径操作，只是声明 URL
- 该信息会出现在 OpenAPI 文档和 Swagger UI 中

### 3. 使用 OAuth2PasswordBearer

```python
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

**工作原理：**
1. 检查请求的 `Authorization` header
2. 验证格式是否为 `Bearer <token>`
3. 提取并返回 token 字符串
4. 如果无效，自动返回 401 错误

### 4. Swagger UI 集成

使用 `OAuth2PasswordBearer` 后，Swagger UI 自动显示：

- "Authorize" 按钮
- 路径操作右上角的小锁图标
- 认证表单（输入 username/password）

### 5. 依赖注入链

```
请求 -> OAuth2PasswordBearer -> 提取 token -> 路径操作函数
```

## 实际应用场景

### 场景1：简单 Token 认证

```python
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    # 此处可以验证 token
    return {"message": "Access granted", "token": token}
```

### 场景2：多层依赖

```python
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 验证 token 并返回用户
    user = verify_token(token)
    return user

@app.get("/users/me")
async def read_users_me(user: User = Depends(get_current_user)):
    return user
```

## 重要提示

⚠️ **生产环境必须使用 HTTPS**
- OAuth2 不指定加密方式
- Token 和密码明文传输，必须 HTTPS 保护

⚠️ **需要 python-multipart**
- OAuth2 使用表单数据发送 username/password
- 安装：`pip install python-multipart`

## 快速测试

1. 启动应用：`uvicorn main:app --reload`
2. 访问：http://127.0.0.1:8000/docs
3. 点击 "Authorize" 按钮
4. 输入任意 username/password（暂时不会验证）
5. 访问受保护的端点

## 下一步

- 下一章：Get Current User - 从 token 获取用户信息
- 然后：Simple OAuth2 - 实现完整的登录流程

## 参考资源

- [OAuth2 规范](https://oauth.net/2/)
- [Bearer Token RFC 6750](https://tools.ietf.org/html/rfc6750)
