# 练习62：响应Cookie（Response Cookies）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 设置基本Cookie
要求:
- 创建POST接口 /login/
- 使用 response.set_cookie(key="session_id", value="abc123") 设置Cookie
- 用curl -i 或浏览器开发者工具观察Set-Cookie响应头
"""

"""
任务2: Cookie安全参数
要求:
- 再次set_cookie，带上参数：max_age=3600, expires=..., httponly=True, secure=False, samesite="lax"
- 在注释中回答：每个参数的作用分别是什么
"""

"""
任务3: 在依赖中设置Cookie
要求:
- 创建依赖函数，通过注入的Response参数设置一个trace_id Cookie
- 路由同时声明 response: Response 和依赖
- 观察最终响应中两个Cookie是否都生效
"""

"""
任务4: 删除Cookie
要求:
- 创建POST接口 /logout/，使用 response.delete_cookie(key="session_id")
- 测试设置后再删除的效果
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
