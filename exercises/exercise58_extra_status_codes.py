# 练习58：额外状态码（Additional Status Codes）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 声明额外状态码
要求:
- 创建Message模型: message(str)
- 创建GET接口 /items/{item_id}
- 使用 responses={404: {"model": Message, "description": "未找到该条目"}} 声明
- item_id不为"foo"时返回数据，否则抛出HTTPException(404)
"""

"""
任务2: 组合多个额外状态码
要求:
- 创建接口的responses同时声明404和403两种情况
- 403返回模型Message，描述为"权限不足"
- 用查询参数role模拟：role!="admin"时抛出403
"""

"""
任务3: 默认422观察
要求:
- 接收一个int类型参数，传入非法值触发422
- 在 /docs 中观察：422是否自动出现在文档中、额外声明的404/403如何展示
- 在注释中记录：为什么422不需要手动声明
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
