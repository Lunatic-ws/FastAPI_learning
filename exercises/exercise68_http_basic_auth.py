# 练习68：HTTP基本认证（HTTP Basic Auth）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 基本认证方案
要求:
- 使用 HTTPBasic() 创建basic_scheme
- 创建依赖get_username，接收 credentials: HTTPBasicCredentials = Depends(basic_scheme)
- 返回credentials.username
- 在/docs中观察Basic认证的用户名密码输入界面
"""

"""
任务2: 安全比较凭据
要求:
- 使用 secrets.compare_digest 分别比较用户名和密码
- 正确凭据设为"admin"/"password123"
- 在注释中回答：为什么不直接用==比较（提示：时序攻击）
"""

"""
任务3: 401与WWW-Authenticate头
要求:
- 凭据错误时抛出HTTPException(401)
- 设置 headers={"WWW-Authenticate": "Basic"}
- 在注释中回答：这个头的作用是什么
"""

"""
任务4: 受保护接口
要求:
- 创建GET接口 /protected/，依赖get_username返回"欢迎, {username}"
- 用浏览器直接访问测试弹出式登录框的效果
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
