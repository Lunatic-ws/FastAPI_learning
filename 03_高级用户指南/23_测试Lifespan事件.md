# 23 测试Lifespan事件

## 学习目标

- 理解 TestClient 触发 lifespan（启动/关闭事件）的条件
- 掌握对启动时初始化资源的测试方法

## 核心概念

### 1. 被测应用

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.testclient import TestClient

items = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    items["config"] = {"env": "test"}  # 启动时初始化
    yield
    items.clear()  # 关闭时清理

app = FastAPI(lifespan=lifespan)

@app.get("/items")
async def read_items():
    return {"config": items.get("config")}
```

### 2. 关键区别：with 触发 lifespan

```python
client = TestClient(app)

# ✅ 用 with：进入时触发启动事件，退出时触发关闭事件
def test_with_context():
    with client as c:
        response = c.get("/items")
        assert response.json() == {"config": {"env": "test"}}

# ❌ 不用 with：不会触发启动/关闭事件
def test_without_context():
    response = client.get("/items")
    assert response.json() == {"config": None}
```

- `with TestClient(app) as client:` 的**进入**对应 startup（yield 前），**退出**对应 shutdown（yield 后）
- 直接 `client.get(...)` 不走上下文管理器，lifespan 完全不执行——初始化的数据不存在
- 这正是文档中同一测试"两种写法结果不同"的原因

### 3. 测试关闭逻辑

```python
def test_shutdown_cleanup():
    with client:
        assert "config" in items
    # 退出 with 后关闭事件已执行
    assert "config" not in items
```

### 4. 与依赖覆盖配合

启动事件里初始化的资源 + 测试中覆盖依赖是常见组合：

```python
def test_with_override():
    with client as c:
        c.app.dependency_overrides[get_db] = get_test_db
        response = c.get("/users")
        assert response.status_code == 200
        c.app.dependency_overrides.clear()
```

## 最佳实践

1. **测试里永远用 `with client`**：除非明确要测试"未初始化"状态，否则应保证事件触发
2. **把状态断言和接口断言分开**：先验证初始化是否发生，再验证接口行为
3. **fixture 中管理 client 生命周期**：pytest 中把 `with TestClient(app) as c` 包进 fixture，全部测试共享已初始化的 client

## 常见问题

**Q: 为什么我的测试拿不到 lifespan 里初始化的模型/连接？**
A: 八成是没有用 `with` 上下文管理器，startup 代码根本没执行

**Q: 多个测试怎么避免重复执行启动事件？**
A: 在 pytest fixture（scope="module"/"session"）中进入一次 with，所有测试共用

## 相关章节

- [21_Lifespan事件.md](./21_Lifespan事件.md) - Lifespan 事件
- [22_测试WebSockets.md](./22_测试WebSockets.md) - 测试 WebSockets
- [25_异步测试.md](./25_异步测试.md) - 异步测试
