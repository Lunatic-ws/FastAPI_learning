# 练习87：JSON与Base64字节（JSON and Base64 Bytes）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: JSON中的bytes
要求:
- 构造一个包含 bytes 字段的dict，尝试 json.dumps
- 在注释中记录报错信息与原因
"""

"""
任务2: jsonable_encoder转换bytes
要求:
- 使用 jsonable_encoder 编码包含bytes的对象
- 打印结果，观察bytes被转成了什么（base64字符串）
"""

"""
任务3: Pydantic的bytes字段
要求:
- 创建Item模型: name(str), data(bytes)
- 接收包含data的POST请求
- 在注释中回答：客户端应如何编码bytes发送给JSON接口
"""

"""
任务4: base64编码解码
要求:
- 使用 base64.b64encode / b64decode 手动编码一段文本
- 创建接口：接收base64字符串，解码后返回utf-8文本
- 对比手动编码与Pydantic自动处理的差异
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
