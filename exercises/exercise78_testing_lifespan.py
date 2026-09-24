# 练习78：测试Lifespan事件（Testing Events: Lifespan）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 触发lifespan的测试
要求:
- 应用使用lifespan在启动时往全局dict加载"模型"
- 测试中使用 with TestClient(app) as client: 触发startup
- 断言全局资源已加载（不为空）
"""

"""
任务2: 验证接口依赖startup资源
要求:
- 创建GET接口 /model-info/ 返回已加载模型的信息
- 在with块内请求该接口，断言返回正常
"""

"""
任务3: 不触发lifespan的对比
要求:
- 不使用with，直接 client = TestClient(app) 后发请求
- 在注释中记录现象与原因
"""

"""
任务4: shutdown验证
要求:
- 在lifespan的yield之后打印清理日志
- 测试with块结束后，验证清理逻辑被执行（如全局资源被清空）
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
