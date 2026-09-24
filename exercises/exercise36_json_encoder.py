# 练习36：JSON兼容编码器（JSON Compatible Encoder）
# 要求：根据注释要求实现相应的FastAPI应用
# 说明：从 fastapi.encoders 导入 jsonable_encoder

# 题目1：转换包含datetime的模型
# 创建Item模型: name(str), timestamp(datetime)
# 使用 jsonable_encoder(item) 将其转为JSON兼容的字典
# 打印结果，观察datetime被转成了什么格式

# 题目2：转换非JSON原生类型
# 创建一个包含 bytes、set、UUID 的字典
# 使用 jsonable_encoder 转换，打印每个类型的转换结果

# 题目3：存入模拟数据库
# 创建一个内存字典 fake_db = {}
# 用 jsonable_encoder 编码Item后以id为键存入
# 再从fake_db取出返回给客户端

# 题目4：对比model_dump()
# 分别使用 item.model_dump() 和 jsonable_encoder(item)
# 构造一个包含datetime的Item，对比两者输出的差异
# 在注释中回答：为什么存入外部数据库前要用jsonable_encoder

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
