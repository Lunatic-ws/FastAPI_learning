# 29 Security 简介

## 学习目标

- 理解常见安全认证方式
- 了解 OAuth2、OpenID Connect 概念
- 理解 FastAPI 的安全工具
- 掌握 OpenAPI 安全方案

## 核心概念

### 1. OAuth2

OAuth2 是认证和授权的规范，支持多种复杂场景：

- **第三方登录**：Facebook、Google、GitHub 等
- **多种流程（flows）**：
  - `password`：用户名密码认证（适合同应用）
  - `authorizationCode`：授权码模式（第三方应用）
  - `clientCredentials`：客户端凭证
  - `implicit`：隐式模式

**注意：** OAuth2 不指定加密方式，需要 HTTPS

### 2. OpenID Connect

基于 OAuth2 的扩展规范：
- 解决 OAuth2 的歧义性
- 提供标准化用户信息
- Google 登录使用此规范

### 3. OpenAPI 安全方案

OpenAPI 定义多种安全方案：

#### apiKey
- 应用特定密钥
- 来源：查询参数、Header、Cookie

#### http
- 标准 HTTP 认证
- `bearer`：Bearer Token（来自 OAuth2）
- Basic、Digest 认证

#### oauth2
- OAuth2 的各种流程
- `password` flow：适合直接认证
- `authorizationCode`：适合第三方应用

#### openIdConnect
- 自动发现 OAuth2 认证数据
- 基于OpenID Connect规范

### 4. FastAPI 安全工具

FastAPI 提供 `fastapi.security` 模块：

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

**自动功能：**
- 在 OpenAPI 中记录安全方案
- Swagger UI 显示认证输入
- 自动验证请求

### 5. 认证流程概览

#### 简单Bearer Token
1. 客户端登录获取 token
2. 后续请求携带 `Authorization: Bearer <token>`
3. 服务器验证 token

#### OAuth2 Password Flow
1. 客户端发送 `username` + `password`
2. 服务器返回 `access_token`
3. 后续请求使用 Bearer Token
4. Token 可设置过期时间

#### JWT Token
1. Token 包含用户信息（JSON Web Token）
2. 服务器无需存储 token
3. 可验证 token 签名和过期时间

## 安全方案对比

| 方案 | 适用场景 | 复杂度 |
|------|---------|--------|
| API Key | 简单API | 低 |
| HTTP Basic | 内部服务 | 低 |
| Bearer Token | 单应用认证 | 中 |
| OAuth2 | 第三方集成 | 高 |
| JWT | 无状态认证 | 中 |

## FastAPI 安全特性

✅ **内置工具**：`fastapi.security` 模块
✅ **自动集成**：OpenAPI 文档自动更新
✅ **依赖注入**：认证作为依赖使用
✅ **灵活组合**：支持多种认证方式

## 开发建议

1. **生产环境必须使用 HTTPS**
2. **不要存储明文密码**：使用哈希
3. **Token 应设置过期时间**
4. **敏感信息不要放在 URL 中**
5. **使用环境变量存储密钥**

## 下一步

- 下一章：Security First Steps - 第一个安全示例
- 然后：Get Current User - 获取当前用户
- 最后：OAuth2 with JWT - 完整认证系统

## 参考资源

- [OAuth2 规范](https://oauth.net/2/)
- [OpenID Connect](https://openid.net/connect/)
- [JWT.io](https://jwt.io/)
