# 练习75：WebSocket
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 基本WebSocket端点
要求:
- 创建 @app.websocket("/ws") 端点
- 使用 await websocket.accept() 接受连接
- 接收文本消息 await websocket.receive_text() 并回发 "回声: ..."
"""

"""
任务2: 处理断开连接
要求:
- 使用 try/except 捕获 WebSocketDisconnect
- 断开时打印客户端离开信息
- 用浏览器控制台 new WebSocket 测试连接与断开
"""

"""
任务3: 广播聊天室
要求:
- 用一个全局集合管理所有活跃连接
- 实现简易聊天：任一客户端发消息，广播给所有连接
- 某客户端断开时从集合中移除（注意并发遍历安全）
"""

"""
任务4: WebSocket依赖注入
要求:
- 为websocket端点声明一个依赖（如校验查询参数token）
- 校验失败时使用 await websocket.close(code=1008) 拒绝连接
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
