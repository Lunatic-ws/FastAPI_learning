# 练习66: 高级安全
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: HTTP Basic Auth - 基础实现
要求:
- 使用 HTTPBasic 和 HTTPBasicCredentials
- 创建路由 /login/ 要求Basic Auth认证
- 返回当前用户的用户名和密码（实际项目中不应返回密码）
- 使用 secrets.compare_digest 比较用户名和密码
- 验证失败返回401状态码和 WWW-Authenticate header
- 测试用户: username="admin", password="secret123"
"""

"""
任务2: HTTP Basic Auth - 用户验证
要求:
- 创建模拟用户数据库 {"admin": "password123", "user1": "pass456"}
- 实现 get_current_user() 依赖
- 依赖验证用户名和密码是否匹配数据库
- 验证失败抛出 HTTPException
- 创建 /profile/ 路由返回当前用户信息
"""

"""
任务3: OAuth2 Scopes - 基础实现
要求:
- 使用 OAuth2PasswordBearer 定义 scopes
- 定义scopes: "read", "write", "admin"
- 实现 create_token() 路由，接收 username 和 scopes 列表，返回JWT token
- token中包含用户信息和scopes
- 实现 get_current_user() 依赖解析token
"""

"""
任务4: OAuth2 Scopes - 权限验证
要求:
- 实现 require_scopes() 依赖工厂，接收 required_scopes 列表
- 验证用户token中是否包含所有required_scopes
- 权限不足时返回403 Forbidden
- 创建路由:
  - /read-data/ 要求 "read" scope
  - /write-data/ 要求 "write" scope
  - /admin-panel/ 要求 "admin" scope
"""

"""
任务5: OAuth2 Scopes - 完整流程
要求:
- 实现完整的OAuth2流程:
  1. POST /token/ - 用户登录，返回access_token（含scopes）
  2. GET /users/me/ - 返回当前用户信息（要求认证）
  3. GET /items/ - 返回项目列表（要求 "items:read" scope）
  4. POST /items/ - 创建项目（要求 "items:write" scope）
- 使用JWT token，包含 sub（用户ID）和 scopes
- 实现权限验证中间件
"""

"""
任务6: 组合认证 - 多种认证方式
要求:
- 实现支持两种认证方式:
  1. API Key (通过header X-API-Key)
  2. Bearer Token (OAuth2)
- 创建 get_current_user() 依赖，自动检测使用哪种认证
- API Key列表: ["key1", "key2", "key3"]
- 模拟用户数据库，包含用户信息和token
- 路由 /protected/ 支持任意一种认证方式
"""

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
