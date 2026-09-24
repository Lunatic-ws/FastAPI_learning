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

# 题目1：创建用户模型和解析函数
# 实现：
# - User 模型：username (str), email (str|None), full_name (str|None), disabled (bool|None)
# - fake_decode_token(token: str) -> User 函数
#   - 假实现：返回 User(username=token, email="user@example.com", full_name="Test User")

# 题目2：实现 get_current_user 依赖
# 实现：
# - 创建 get_current_user(token: str = Depends(oauth2_scheme)) -> User
# - 调用 fake_decode_token 解析 token
# - 返回 User 对象

# 题目3：创建用户信息端点
# 实现：
# - GET /users/me 返回当前用户（完整 User 对象）
# - GET /users/me/profile 只返回 username 和 full_name
# - 都需要通过 get_current_user 依赖注入

# 题目4：实现活跃用户检查
# 实现：
# - get_current_active_user 依赖
#   - 依赖 get_current_user
#   - 如果 user.disabled 为 True，抛出 HTTPException(400, detail="Inactive user")
# - GET /active-only 端点使用该依赖
#   - 返回 {"message": "Welcome active user", "username": user.username}

# 题目5：错误处理
# 实现：
# - 修改 get_current_user，添加错误处理
# - 如果 token 无效或解析失败，抛出 401 HTTPException
# - 包含 headers={"WWW-Authenticate": "Bearer"}

if __name__ == "__main__":
    pass
