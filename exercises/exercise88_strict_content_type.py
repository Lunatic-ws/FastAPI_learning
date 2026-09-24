# 练习88：严格Content-Type（Strict Content-Type Validation）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 默认的宽松解析
要求:
- 创建接收Pydantic模型的POST接口
- 用curl分别以 application/json 和 text/plain 发送相同的JSON内容
- 在注释中记录：默认情况下FastAPI是否严格校验Content-Type
"""

"""
任务2: 用Request手动严格校验
要求:
- 创建POST /strict/ 接口，注入request: Request
- 检查 request.headers["content-type"] 是否为 application/json
- 不匹配时抛出 HTTPException(status_code=415, detail="不支持的Content-Type")
"""

"""
任务3: 读取原始body并手动解析
要求:
- 在校验通过后 await request.body() 并 json.loads 解析
- 手动构造模型实例返回
"""

"""
任务4: 特性背景理解
要求:
- 在注释中回答：新版本FastAPI提供的严格Content-Type校验解决了什么问题
- 在什么业务场景下需要严格校验（如网关、Webhook验签）
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
