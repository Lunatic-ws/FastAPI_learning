# 33 严格ContentType

## 学习目标

- 理解 FastAPI 对 JSON 请求的严格 `Content-Type` 检查
- 掌握该默认行为防御的 CSRF 攻击场景
- 学会在必要时关闭严格检查

## 核心概念

### 1. 默认行为

FastAPI 对 JSON 请求体使用**严格的 `Content-Type` 头检查**：JSON 请求必须带有效的 `Content-Type`（如 `application/json`），请求体才会被按 JSON 解析。此行为和配置在 **FastAPI 0.132.0** 中新增。

没有合法 `Content-Type` 的请求 → 不会被解析为 JSON 请求体。

### 2. 为什么：CSRF 风险

浏览器允许脚本在某些条件下**不做 CORS 预检**直接发送请求：

- 没有 `Content-Type` 头（如 `fetch()` 携带 `Blob` 作为 body）
- 且不发送任何认证凭据

这类攻击主要相关于：**应用运行在本地/内网 + 没有任何认证**，即"信任同一网络的所有请求"。

### 3. 攻击示例

假设一个本地 AI 代理：

- API：`http://localhost:8000/v1/agents/multivac`
- 前端：`http://localhost:8000`（同主机）
- 因为只在本地运行，不做任何认证，信任本地网络

用户安装后打开了恶意网站 `https://evilhackers.example.com`，其中脚本用 `fetch()` + `Blob` body 向 `http://localhost:8000/v1/agents/multivac` 发请求：

- 不涉及认证凭据 → 无需 CORS 预检
- 缺少 `Content-Type` → 浏览器认为不是 JSON

恶意网站就可能操纵本地 AI 代理替用户执行操作（发消息、改配置等）。😅

严格检查的默认行为会拒绝这种无 `Content-Type` 的请求体，切断该攻击路径。

### 4. 开放的互联网不适用

应用部署在公网时：

- 本就不会"信任网络"，特权端点都应有认证
- 攻击者可以脱离浏览器直接对 API 发脚本请求，无需借助 CSRF

因此该风险主要针对"本地网络 + 仅依赖网络隔离"的应用。

### 5. 关闭严格检查

需要兼容不发送 `Content-Type` 的客户端时：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(strict_content_type=False)

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return item
```

关闭后，缺少 `Content-Type` 头的请求体也会按 JSON 解析（与旧版本 FastAPI 行为一致）。

## 最佳实践

1. **保持默认开启**：除非明确要支持不发 `Content-Type` 的老旧客户端
2. **本地/内网工具同样要有认证**：不要只依赖网络隔离
3. **公网应用该风险基本不适用**：正常认证 + HTTPS 下无需为此关闭/调整

## 常见问题

**Q: 升级后老客户端突然 422 了？**
A: 检查客户端是否带 `Content-Type: application/json`；无法改客户端时用 `strict_content_type=False` 回退旧行为

**Q: 这个检查和 CORS 预检的关系？**
A: 检查发生在 FastAPI 应用层，与浏览器 CORS 无关；它防的是"浏览器跳过预检直接发出的无 Content-Type 请求"

## 相关章节

- [16_高级中间件.md](./16_高级中间件.md) - 中间件与 CORS
- [18_位于代理后.md](./18_位于代理后.md) - 代理与信任边界
- [14_直接使用Request.md](./14_直接使用Request.md) - 直接使用 Request
