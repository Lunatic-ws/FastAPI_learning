# 29 包含WSGI

## 学习目标

- 掌握在 FastAPI/Starlette 应用中挂载 WSGI 应用（Flask/Django）
- 理解 ASGI 与 WSGI 的互操作方式

## 核心概念

### 1. 场景

已有 Flask/Django 等传统 WSGI 应用，想渐进迁移到 FastAPI：新旧共存于同一个域名下，共享一个部署入口。

### 2. 挂载 WSGI 中间件

WSGI 应用不能直接跑在 ASGI 服务器上，需要适配层。FastAPI 文档使用 `a2wsgi`：

```bash
pip install a2wsgi
```

```python
from fastapi import FastAPI
from a2wsgi import WSGIMiddleware
from flask import Flask, request

flask_app = Flask(__name__)

@flask_app.route("/")
def flask_main():
    name = request.args.get("name", "World")
    return f"Hello, {name} from Flask!"

app = FastAPI()

@app.get("/items/{id}")
async def read_item(id: int):
    return {"item_id": id, "from": "FastAPI"}

# 把 WSGI 应用包一层再 mount
app.mount("/flask", WSGIMiddleware(flask_app))
```

- 访问 `/items/5` 由 FastAPI 处理（JSON）
- 访问 `/flask?name=Alice` 由 Flask 处理（HTML）
- 挂载路径下的**所有**请求都交给子应用

### 3. Django 同理

```python
from a2wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application

django_application = get_wsgi_application()
app.mount("/django", WSGIMiddleware(django_application))
```

### 4. 工作原理

- 服务器（uvicorn）以 ASGI 协议与 FastAPI 通信
- 请求进入挂载路径后，`WSGIMiddleware` 把 ASGI 环境转换成 WSGI environ，调用 Flask/Django
- 响应再转换回 ASGI 返回

## 最佳实践

1. **迁移期共存，别长期共存**：逐模块把 Flask 蓝图迁移成 FastAPI 路由，缩小 WSGI 边界
2. **挂载路径规划好**：WSGI 应用拿到的是挂载前缀之后的路径（`SCRIPT_NAME` 机制），注意 Flask 路由书写
3. **Django 全家桶**：settings、中间件、数据库配置照常由 Django 自己管理

## 常见问题

**Q: 流式响应/长连接支持吗？**
A: WSGI 天生不支持 WebSocket，其响应是阻塞一次性完成的；需要流式/推送的部分要迁到 ASGI 侧

**Q: 用别的适配器行吗？**
A: 可以（如早年的 `a2wsgi` 之前社区方案），FastAPI 文档目前推荐 `a2wsgi`

## 相关章节

- [17_子应用挂载.md](./17_子应用挂载.md) - 子应用挂载
- [36_SQL数据库.md](../02_教程-用户指南/36_SQL数据库.md) - SQL 数据库
- [18_位于代理后.md](./18_位于代理后.md) - 代理部署
