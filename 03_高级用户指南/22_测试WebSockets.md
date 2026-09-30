# 22 测试WebSockets

## 学习目标

- 掌握用 TestClient 测试 WebSocket 端点
- 理解 `websocket_connect` 的会话式用法

## 核心概念

### 1. 被测应用

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()

@app.websocket("/ws/echo")
async def websocket_echo(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

### 2. 基本测试：连接 → 收发 → 断开

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_websocket():
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
```

- 必须用 `with` 上下文管理器：进入时建立连接，退出时清理
- `send_json` / `receive_json`、`send_text` / `receive_text` 成对使用

### 3. 回显（交互循环）测试

```python
def test_websocket_echo():
    with client.websocket_connect("/ws/echo") as websocket:
        websocket.send_text("Hello")
        assert websocket.receive_text() == "Message text was: Hello"
        websocket.send_text("World")
        assert websocket.receive_text() == "Message text was: World"
```

- 收发按顺序一一对应，测试代码就是模拟一个客户端会话

### 4. 带查询参数与依赖

WebSocket 端点可以使用查询参数和依赖注入，测试时直接拼在 URL 上：

```python
@app.websocket("/ws/items")
async def ws_items(websocket: WebSocket, q: str = "", token: str = Depends(auth)):
    ...

def test_with_query():
    with client.websocket_connect("/ws/items?q=abc&token=x") as ws:
        ...
```

## 最佳实践

1. **with 语句包裹会话**：保证连接正常关闭、异常时有清理
2. **按协议顺序断言**：服务端发什么、按什么顺序发，测试要严格对应
3. **分离消息格式测试**：JSON 结构与业务逻辑分开断言，便于定位失败原因

## 常见问题

**Q: 不用 with 直接 websocket_connect 会怎样？**
A: 连接不会被显式关闭，可能产生悬挂连接和资源泄漏

**Q: 能测试连接被拒绝的场景吗？**
A: 能，服务端未 `accept` 直接 `close` 时，客户端 receive 会抛出 `WebSocketDisconnect`

## 相关章节

- [20_WebSocket.md](./20_WebSocket.md) - WebSocket 端点
- [23_测试Lifespan事件.md](./23_测试Lifespan事件.md) - 测试 lifespan 事件
- [24_测试依赖覆盖.md](./24_测试依赖覆盖.md) - 依赖覆盖
