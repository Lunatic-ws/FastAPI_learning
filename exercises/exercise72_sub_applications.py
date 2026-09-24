# 练习72：子应用挂载（Sub Applications - Mounts）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 挂载子应用
要求:
- 创建主应用app和一个子应用subapi = FastAPI()
- 子应用中有自己的接口（如GET /items/）
- 使用 app.mount("/subapi", subapi) 挂载
"""

"""
任务2: 子应用的文档
要求:
- 访问 /subapi/docs 查看子应用独立的文档
- 对比主应用 /docs
- 在注释中记录两者的接口列表差异
"""

"""
任务3: 多级子应用
要求:
- 再创建一个admin子应用挂载到 /admin
- 主应用、subapi、admin各自有不同接口
- 用curl分别访问三个路径验证路由归属
"""

"""
任务4: mount与APIRouter的区别
要求:
- 在注释中回答：mount和include_router分别适合什么场景
- mount的子应用有哪些独立于主应用的配置（docs、中间件等）
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
