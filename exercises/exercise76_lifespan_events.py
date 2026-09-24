# 练习76：Lifespan事件（Lifespan Events）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 基本lifespan
要求:
- 使用 @asynccontextmanager 定义 async def lifespan(app: FastAPI)
- yield之前的代码在启动时执行，之后的代码在关闭时执行
- 创建FastAPI(app=..., lifespan=...) 注册
- 启动和停止服务，观察打印顺序
"""

"""
任务2: 模拟加载ML模型
要求:
- 定义全局变量 ml_models = {}
- lifespan启动阶段往ml_models放入一个"模型"对象（dict即可）
- 创建GET接口 /predict/ 使用该模型返回结果
- 关闭阶段清空ml_models
"""

"""
任务3: 启动失败的传播
要求:
- 在yield之前抛出一个异常，观察服务无法启动
- 在注释中回答：lifespan中抛异常意味着什么
"""

"""
任务4: 对比旧写法
要求:
- 在注释中回答：@app.on_event("startup") 与lifespan的关系
- 为什么官方推荐lifespan（提示：资源可共享、代码可在yield前后组织）
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
