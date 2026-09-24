# 练习67：OAuth2作用域（OAuth2 Scopes）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 声明作用域
要求:
- 创建OAuth2PasswordBearer，scopes参数声明：
  items: read / items: write / users: read
- 在/docs的Authorize面板中观察scopes勾选框
"""

"""
任务2: 创建带scopes的token
要求:
- POST /token/ 接收OAuth2PasswordRequestForm，form.scopes即选中的作用域列表
- 将scopes写入JWT的"scopes"声明中
"""

"""
任务3: 校验作用域
要求:
- get_current_user依赖中接收 security_scopes: SecurityScopes 参数
- 解码JWT后逐层检查token中的scopes是否覆盖security_scopes.scopes
- 使用 Security(get_current_user, scopes=["items:read"]) 声明接口依赖
"""

"""
任务4: 权限不足返回403
要求:
- scopes不满足时抛出HTTPException(403)，detail中带上缺失的scopes
- 创建3个接口验证：/items/（读）、/items-write/（写）、/users/（用户读）
- 分别以不同scopes组合的token测试
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
