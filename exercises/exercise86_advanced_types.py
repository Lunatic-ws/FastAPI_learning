# 练习86：高级Python类型（Advanced Python Types）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: Annotated与元数据
要求:
- 使用 Annotated[int, Query(gt=0, description="页码")] 声明参数
- 对比 Annotated 与默认值参数两种写法的可读性
"""

"""
任务2: Literal类型
要求:
- 使用 Literal["small", "medium", "large"] 限定查询参数size取值
- 传入非法值观察422错误中Allowed values的展示
"""

"""
任务3: 泛型模型
要求:
- 定义泛型类 Page(BaseModel, Generic[T])，包含 items: list[T]、total: int
- 用 Page[Item] 和 Page[User] 分别作为两个接口的返回类型注解
- 观察文档中两个接口的响应模型是否正确展开
"""

"""
任务4: TypedDict与嵌套结构
要求:
- 使用 TypedDict 定义一个嵌套字典结构并作为请求体
- 在注释中回答：TypedDict与Pydantic模型在验证上的区别
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
