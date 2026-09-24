# 练习40：Security First Steps

"""
要求：
1. 创建一个 FastAPI 应用
2. 使用 OAuth2PasswordBearer 实现 token 认证
3. 创建一个受保护的端点，返回 token 内容
4. 验证 Swagger UI 显示 Authorize 按钮

知识点：
- OAuth2PasswordBearer 初始化
- tokenUrl 参数含义
- Depends 注入 token
- 自动 401 错误处理
"""

# 题目1：创建基础安全应用
# 实现：
# - 创建 FastAPI 应用
# - 初始化 OAuth2PasswordBearer，tokenUrl 设为 "token"
# - 创建 GET /items/ 端点，接收 token 参数（通过 Depends）
# - 返回 {"token": token}

# 题目2：创建多个受保护端点
# 实现：
# - GET /protected/ 端点，返回 {"message": "This is protected", "token": <token>}
# - GET /admin/ 端点，返回 {"role": "admin", "token": <token>}
# - 都需要通过 OAuth2PasswordBearer 认证

# 题目3：自定义 tokenUrl
# 实现：
# - 创建新的 OAuth2PasswordBearer，tokenUrl 设为 "/api/v1/login"
# - 创建 GET /secure-data/ 端点使用该 scheme
# - 返回 {"data": "sensitive", "authenticated": True}

if __name__ == "__main__":
    pass
