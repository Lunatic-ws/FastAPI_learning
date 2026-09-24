# 练习63：响应Headers（Response Headers）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 设置自定义响应头
要求:
- 创建GET接口 /headers/
- 路由函数声明 response: Response 参数
- 设置 response.headers["X-Custom-Header"] = "custom-value"
- 用curl -i观察响应头
"""

"""
任务2: 预先声明响应头（文档可见）
要求:
- 在路径操作装饰器中使用 headers 参数（通过responses或openapi_extra声明）
- 使自定义头出现在 /docs 的响应文档中
- 在注释中说明：只在函数内设置头时为什么文档中看不到
"""

"""
任务3: 在依赖中设置响应头
要求:
- 创建依赖函数通过注入的response参数设置 X-Process-Time 头
- 用time.perf_counter()记录处理耗时写入头
- 多个接口复用该依赖
"""

"""
任务4: 返回后才确定值的头
要求:
- 在注释中回答：为什么生成响应后才能设置的值（如Content-Length）
- 需要使用什么机制（提示：与后台任务/中间件结合）
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
