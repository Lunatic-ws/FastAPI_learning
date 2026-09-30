# 08 响应Headers

## 学习目标

- 掌握在响应中添加自定义 Header
- 理解 Header 与 OpenAPI 文档的关系

## 核心概念

### 1. 注入 Response 参数

与 Cookie 类似，声明 `Response` 参数后直接赋值：

```python
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/headers/")
async def read_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello World"}
```

- 可以正常返回字典/Pydantic 模型等，Header 会合并进最终响应
- 自定义 Header 约定用 `X-` 前缀（如 `X-Cat-Dog`），与标准 Header 区分

### 2. 直接返回 Response 时设置

```python
from fastapi.responses import JSONResponse

@app.get("/direct/")
async def direct():
    response = JSONResponse(content={"message": "hello"})
    response.headers["X-Custom"] = "value"
    return response
```

### 3. 使用场景

- **追踪与审计**：`X-Request-ID`（链路追踪）
- **缓存控制**：`Cache-Control`、`ETag`
- **安全加固**：`X-Content-Type-Options`、`X-Frame-Options`
- **限流信息**：`X-RateLimit-Remaining`（通常配合中间件统一处理）

### 4. 在中间件中统一设置

单个端点的 Header 用 `Response` 参数；全站 Header 放中间件：

```python
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
```

## 最佳实践

1. **端点级用 Response 参数，全局级用中间件**
2. **标准 Header 不要乱造**：自定义信息 Header 用 `X-` 前缀，避免与既有规范冲突
3. **值必须是字符串**：`response.headers["X-Count"] = str(count)`

## 常见问题

**Q: 自定义 Header 会出现在 Swagger 文档里吗？**
A: 不会自动出现在响应定义中；需要在 `responses={200: {"headers": {...}}}` 中显式声明才会进文档

**Q: 浏览器读不到自定义 Header？**
A: 跨域时需在 CORS 中间件的 `expose_headers` 中列出该 Header，否则前端 JS 无法读取

## 相关章节

- [07_响应Cookie.md](./07_响应Cookie.md) - 响应 Cookie
- [16_高级中间件.md](./16_高级中间件.md) - 高级中间件
- [05_自定义Response.md](./05_自定义Response.md) - 自定义响应类
