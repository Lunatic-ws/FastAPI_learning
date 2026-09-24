# 练习42：简单OAuth2
# 要求：根据注释要求实现相应的FastAPI应用
# 说明：使用 OAuth2PasswordBearer 和 OAuth2PasswordRequestForm

# 题目1：创建OAuth2方案
# 使用 OAuth2PasswordBearer(tokenUrl="token") 创建 oauth2_scheme
# 在 /docs 中观察出现Authorizate按钮的效果

# 题目2：模拟用户数据库与当前用户
# 创建fake_users_db = {"alice": {"username": "alice", "full_name": "Alice Wang", "email": "alice@example.com"}}
# 创建get_current_user依赖：接收 token: str = Depends(oauth2_scheme)
# token格式为"alice-secret"时返回用户，否则返回None

# 题目3：登录端点颁发token
# 创建POST接口 /token/
# 接收 OAuth2PasswordRequestForm 表单（username、password）
# username存在且password为"secret"时，返回 {"access_token": username + "-secret", "token_type": "bearer"}

# 题目4：受保护接口
# 创建GET接口 /users/me/，依赖get_current_user返回用户信息
# 用户为None时抛出 HTTPException(401)，并设置 headers={"WWW-Authenticate": "Bearer"}
# 使用 /docs 的Authorize流程完整测试登录与访问

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
