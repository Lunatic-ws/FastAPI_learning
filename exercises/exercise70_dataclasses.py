# 练习70：Dataclasses（数据类）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: dataclass作为请求体
要求:
- 使用 @dataclass 定义Item: name(str), price(float), description(可选str)
- 在POST接口中直接作为参数类型接收
- 在注释中回答：FastAPI如何为dataclass生成文档
"""

"""
任务2: dataclass作为依赖
要求:
- 使用 @dataclass 定义PaginationParams: page(int=1), size(int=10)
- 作为依赖使用 Depends(PaginationParams)（也可用Annotated）
- 创建GET接口 /items/ 返回分页参数内容
"""

"""
任务3: Pydantic与dataclass混用
要求:
- 同一接口中同时使用Pydantic模型接收请求体、dataclass接收查询参数
- 观察各自的验证行为差异（dataclass不做类型验证）
"""

"""
任务4: 对比总结
要求:
- 在注释中回答：dataclass与Pydantic模型分别适合什么场景
- dataclass的默认值和字段验证有什么限制
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
