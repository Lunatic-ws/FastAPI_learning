# 28 OpenAPIWebhooks

## 学习目标

- 理解 Webhooks：你作为"服务方"主动通知外部订阅者
- 掌握 `app.webhooks` 声明应用级 webhook 文档

## 核心概念

### 1. Webhooks 与普通接口的关系

Webhooks 场景：你的应用（如 GitHub 一样）对外承诺"当某事件发生时，我会向订阅者提供的 URL 发送一个请求"。

- 这些请求的目标**不在你的应用里**，而是外部系统的地址
- 但为了让订阅方知道"你会发什么结构的数据"，需要在你的 OpenAPI 文档中声明它们
- OpenAPI 3.1+ 专门为此提供了 `webhooks` 字段

### 2. 声明 webhook

用 `app.webhooks` 装饰器声明（同样不写实际逻辑，仅生成文档）：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: str

class InvoiceEvent(BaseModel):
    description: str
    paid: bool

class InvoiceEventReceived(BaseModel):
    ok: bool

@app.webhooks.post("new-subscription")
def new_subscription(body: Subscription):
    """
    当有新用户订阅时，我们会向订阅方提供的 URL 发送
    包含 Subscription 请求体的 POST 请求。
    """

@app.webhooks.post("invoice-paid")
def invoice_paid(body: InvoiceEvent) -> InvoiceEventReceived:
    """
    当发票支付完成后，我们会向订阅方提供的 URL 发送
    InvoiceEvent，并期待收到 InvoiceEventReceived 确认。
    """
```

- URL 路径是**逻辑名称**（如 `new-subscription`），不对应真实端点
- FastAPI 会在 `openapi.json` 中写入 `webhooks` 字段，`/docs` 会展示 "Webhooks" 区块

### 3. 实际发送逻辑在业务代码里

声明只管文档，真正发请求要用 HTTP 客户端：

```python
import httpx

async def notify_invoice_paid(subscriber_url: str, event: InvoiceEvent):
    async with httpx.AsyncClient() as client:
        resp = await client.post(subscriber_url, json=event.model_dump())
        # 可加超时、重试、签名等
```

### 4. 回调 vs Webhooks

| | OpenAPI 回调（callbacks） | Webhooks |
|---|---|---|
| 挂载位置 | 具体某个路径操作 | 应用级（`app.webhooks`） |
| 目标 URL | 每次请求动态决定（`{$callback_url}`） | 由订阅方在业务上预先登记 |
| 典型场景 | 支付网关按请求回调 | 平台事件广播（新订阅、退款等） |

## 最佳实践

1. **文档与实现保持同步**：webhook 请求体改字段时同步更新声明模型
2. **发送时加签名**：在请求头带上 HMAC 签名，让订阅方能验证请求确实来自你
3. **幂等与重试**：订阅方可能重复收到通知，事件里带唯一 ID 便于对方去重

## 常见问题

**Q: app.webhooks 声明的路径能被直接请求吗？**
A: 不能。它只存在于 openapi.json 的 webhooks 字段里，应用中没有对应路由

**Q: Swagger UI 里能看到 Webhooks 吗？**
A: 能，文档页会显示 Webhooks 区块及请求/响应模型

## 相关章节

- [27_OpenAPI回调.md](./27_OpenAPI回调.md) - OpenAPI 回调
- [06_OpenAPI额外响应.md](./06_OpenAPI额外响应.md) - 额外响应
- [37_大型应用结构.md](../02_教程-用户指南/37_大型应用结构.md) - 大型应用结构
