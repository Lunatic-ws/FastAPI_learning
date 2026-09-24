# 练习52：前端（Frontend）
# 要求：根据注释要求实现相应的FastAPI应用

# 题目1：认识app.frontend()
# 在注释中回答：app.frontend() 的作用是什么
# 它是如何把前端构建产物与后端API一起提供的

# 题目2：为独立前端配置CORS
# 创建FastAPI应用并配置CORSMiddleware
# allow_origins=["http://localhost:5173"]（模拟Vite开发服务器）
# 允许的methods为 ["*"]，allow_headers为 ["*"]

# 题目3：提供API供前端调用
# 创建GET接口 /api/data/ 返回 {"items": ["装修", "设计", "施工"]}
# 创建POST接口 /api/echo/ 接收message(str)并原样返回

# 题目4：跨域流程理解（在注释中回答）
# 浏览器在什么情况下会发起CORS预检(OPTIONS)请求
# 如果前端报错CORS policy: No 'Access-Control-Allow-Origin'，应如何排查

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
