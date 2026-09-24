# 练习69：直接使用Request对象（Using the Request Directly）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 注入Request对象
要求:
- 创建GET接口 /inspect/
- 函数声明 request: Request 参数
- 返回 request.method、request.url 的字符串形式、request.headers.get("user-agent")
"""

"""
任务2: 读取客户端信息
要求:
- 返回 request.client.host 和 request.client.port
- 用curl测试并记录结果
"""

"""
任务3: 读取原始请求体
要求:
- 创建POST接口 /raw-body/
- 使用 body = await request.body() 读取原始字节
- 返回字节数量和前100个字符
"""

"""
任务4: Request与声明式接收对比
要求:
- 创建两个接口：一个用Pydantic模型接收JSON，一个用request.json()手动解析
- 在注释中回答：各自丢失/获得了什么（验证、文档、类型提示等）
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
