# 21 Lifespan事件

## 学习目标

- 掌握 `lifespan` 上下文管理器管理启动/关闭逻辑
- 理解其替代 `@app.on_event` 的原因与用法

## 核心概念

### 1. lifespan 函数

用 `@asynccontextmanager` 定义，`yield` 之前的代码在**启动时**执行，之后的代码在**关闭时**执行：

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

def fake_answer_to_everything_ml_model(x: float):
    return x * 42

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动（yield 之前）：加载模型、建立连接池等
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # 关闭（yield 之后）：清理资源
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

- `yield` 前后的代码顺序对应 startup / shutdown
- 整个应用生命周期内只执行一次
- 请求到达时模型已加载完毕

### 2. 典型用途

| 启动时（yield 前） | 关闭时（yield 后） |
|---|---|
| 加载 ML 模型 | 释放模型内存 |
| 建立数据库连接池 | 关闭连接池 |
| 初始化 Redis 客户端 | 断开连接 |
| 预热缓存 | 刷盘/上报指标 |

### 3. 状态传递

可以借助 `app.state` 或模块级变量在 lifespan 与路径操作之间共享对象：

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = create_db_pool()
    yield
    await app.state.db.close()

# 路径操作中
async def handler(request: Request):
    pool = request.app.state.db
```

### 4. 旧式事件（了解即可）

```python
@app.on_event("startup")
async def startup_event(): ...
```

已废弃（deprecated），仅用于阅读旧代码；新项目一律用 `lifespan`。

### 5. 子应用与测试中的 lifespan

- `subapp` 挂载时其 lifespan 会在应用启动时执行
- 测试时用 `with TestClient(app) as client:` 上下文管理器才会触发 lifespan（见"测试Lifespan事件"一节）

## 最佳实践

1. **重资源启动时加载**：避免每个请求重复初始化
2. **yield 后必须清理对称资源**：启动开了什么，关闭就关什么
3. **一个 lifespan 管理全部**：多个资源可用 `AsyncExitStack` 组合多个上下文管理器

## 常见问题

**Q: lifespan 和中间件的区别？**
A: lifespan 按应用生命周期执行一次；中间件每个请求都执行

**Q: 启动逻辑报错会怎样？**
A: yield 之前抛异常会阻止应用启动，适合把配置错误尽早暴露

**Q: on_event 还能用吗？**
A: 能但已废弃，官方建议迁移到 lifespan

## 相关章节

- [23_测试Lifespan事件.md](./23_测试Lifespan事件.md) - 测试 lifespan
- [22_测试WebSockets.md](./22_测试WebSockets.md) - 测试 WebSockets
- [16_高级中间件.md](./16_高级中间件.md) - 中间件
