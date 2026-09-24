# 练习84：包含WSGI（Including WSGI - Flask, Django, others）
# 说明：WSGIMiddleware来自 fastapi.middleware.wsgi
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 定义简单WSGI应用
要求:
- 编写一个符合WSGI标准的函数 wsgi_app(environ, start_response)
- 返回b"Hello from WSGI!"
- （可选：用Flask实现同样的应用，需 pip install flask）
"""

"""
任务2: 用WSGIMiddleware包装
要求:
- wsgi_middleware = WSGIMiddleware(wsgi_app)
"""

"""
任务3: 挂载到FastAPI
要求:
- 使用 app.mount("/v1", wsgi_middleware) 挂载
- 用curl访问 /v1/ 验证返回WSGI应用的内容
"""

"""
任务4: 混合调用
要求:
- 主应用同时有FastAPI原生接口和挂载的WSGI应用
- 在注释中回答：什么场景下需要同时运行两代框架的应用
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
