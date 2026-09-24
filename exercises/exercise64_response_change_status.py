# 练习64：响应更改状态码（Change Status Code）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 默认状态码与声明状态码
要求:
- 创建POST接口 /items/，不声明status_code，观察默认是200
- 创建POST接口 /items2/，声明 status_code=201
- 用curl -i对比两者的响应状态码
"""

"""
任务2: 运行时更改状态码
要求:
- 路由声明 response: Response 参数
- 创建/更新成功时设置 response.status_code = 201
- 资源已存在时设置 response.status_code = 200 并返回已存在数据
- 验证同一接口可返回不同状态码
"""

"""
任务3: 文档中的状态码展示
要求:
- 声明status_code=201的接口在/docs中的默认响应如何展示
- 在注释中回答：运行时改状态码会影响文档吗
"""

"""
任务4: 错误状态码
要求:
- 用HTTPException抛出404，观察其状态码来源
- 在注释中回答：HTTPException的状态码与声明的status_code有什么关系
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
