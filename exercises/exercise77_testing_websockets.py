# 练习77：测试WebSockets（Testing WebSockets）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 用TestClient连接WebSocket
要求:
- 先实现一个简单的 /ws 回声端点（见练习75）
- 使用 with TestClient(app) as client: 包裹
- 使用 client.websocket_connect("/ws") 建立连接
"""

"""
任务2: 收发消息测试
要求:
- 使用 websocket.send_text("hello") 与 websocket.receive_text()
- 断言回声内容正确
- 尝试 send_json / receive_json 的方式测试JSON消息
"""

"""
任务3: 测试断开场景
要求:
- 客户端调用 websocket.close() 后
- 服务端应捕获WebSocketDisconnect
- 在注释中记录如何确认服务端正确处理了断开（如通过日志）
"""

"""
任务4: 整理测试结构
要求:
- 把上述测试组织成 pytest 测试函数
- 在注释中回答：为什么websocket测试必须在 with TestClient 块内
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
