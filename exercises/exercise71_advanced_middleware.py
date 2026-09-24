# 练习71：高级中间件（Advanced Middleware）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 纯ASGI中间件
要求:
- 编写一个纯ASGI中间件函数 async def asgi_middleware(app, scope, receive, send)
- 在调用app(scope, receive, send)前后各打印一行日志
- 使用 app.middleware("http") 之外的方式：直接 app.add_middleware 或包裹
- （提示：BaseHTTPMiddleware包装或自定义类实现__call__）
"""

"""
任务2: BaseHTTPMiddleware类方式
要求:
- 创建类TimingMiddleware继承BaseHTTPMiddleware
- override async def dispatch(self, request, call_next)
- 记录处理耗时并写入 X-Process-Time 响应头
- add_middleware注册
"""

"""
任务3: 多个中间件的执行顺序
要求:
- 创建3个简单日志中间件A、B、C，依次add_middleware注册
- 请求时观察打印顺序
- 在注释中回答：请求和响应阶段各按什么顺序执行
"""

"""
任务4: 中间件短路
要求:
- 编写一个中间件：请求头缺少 x-api-key 时直接返回403，不调用call_next
- 验证合法key时正常放行
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
