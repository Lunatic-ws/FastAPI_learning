# 练习80：异步测试（Async Tests）
# 说明：需要 pip install pytest pytest-asyncio httpx
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 第一个异步测试
要求:
- 使用 pytest-asyncio 的 @pytest.mark.asyncio（或anyio插件方式）标记异步测试函数
- 在注释中说明：为什么不能用TestClient跑异步的断言场景，而要用AsyncClient
"""

"""
任务2: AsyncClient + ASGITransport
要求:
- 使用 httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
- 在异步测试函数中 await client.get("/items/")
- 断言状态码与响应JSON
"""

"""
任务3: 测试异步端点的并发行为
要求:
- 实现一个async接口，内部await asyncio.sleep(1)后返回
- 用asyncio.gather并发请求3次
- 断言总耗时应远小于3秒（证明是并发处理）
"""

"""
任务4: 异步fixture
要求:
- 编写一个async的pytest fixture（如异步准备测试数据）
- 在测试中使用该fixture
- 在注释中记录运行命令：pytest -s 的输出观察点
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
