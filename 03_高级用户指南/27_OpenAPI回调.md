# 27 OpenAPI回调

## 学习目标

- 理解"回调"：你的应用在运行时**调用外部系统**的接口
- 掌握用 `callbacks` 参数把这些调用写进 OpenAPI 文档

## 核心概念

### 1. 回调是什么

常规 API 是"别人调你"；回调相反——你的应用收到请求后，要在某个时刻**主动调用**外部系统（通常是对方预留的 webhook URL）。例如支付网关：你调用它创建订单，它完成支付后回调你预留的地址。

OpenAPI 无法自动知道你会调用什么，所以要**手动声明**，供外部系统生成文档/客户端。

### 2. 声明回调 API

回调接口本身写成"伪路径操作"——用 APIRouter 装饰器声明但**不写实际处理函数体**：

```python
invoices_external_callback_router = APIRouter()

@invoices_external_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}",
    name="invoice_notification",
)
def invoice_notification(body: InvoiceEvent):
    """支付完成后，本应用会向该 URL 发送此请求体"""
    pass  # 永远不会被执行，仅用于生成文档

callback_router = APIRouter()
callback_router.include_router(invoices_external_callback_router)
```

### 3. 在路径操作中使用

```python
class InvoiceEvent(BaseModel):
    id: str
    amount: float
    customer: EmailStr

class InvoiceEventReceived(BaseModel):
    ok: bool

invoices_callback_router = APIRouter()

@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}",
    name="invoice_notification",  # 显示在文档中的回调名
)
def invoice_notification(body: InvoiceEvent) -> InvoiceEventReceived:
    """FastAPI 将在支付完成后，用此请求体调用 $callback_url"""
    pass

@app.post("/invoices/", callbacks=invoices_callback_router.routes)
async def create_invoice(invoice: Invoice):
    """
    创建发票。

    支付网关会在收到后回调 `$callback_url`。
    """
    # 实际业务：向 http://example.com/invoices/ 发请求创建发票
    ...
```

- `callbacks=router.routes` 传入路由列表
- URL 模板中的特殊变量：
  - `{$callback_url}`：对方提供、请求体中带来的回调地址
  - `{$request.body.id}`：引用本次请求体中的字段值
- `pass` 函数体不会被执行，纯粹是文档声明

### 4. 文档效果

`/docs` 中该接口会出现 "Callbacks" 区块，展示回调的 URL 模板、方法、请求/响应模型，外部团队据此知道你们会往哪发、发什么结构。

## 最佳实践

1. **回调也用 Pydantic 建模**：请求体和响应体都声明清楚，别让对接方猜
2. **回调与普通接口分开 router**：语义清晰，复用方便
3. **超时与重试由你的 HTTP 客户端负责**：OpenAPI 只管文档，不保证调用行为

## 常见问题

**Q: 回调处理函数需要实现吗？**
A: 不需要。它只是声明文档的"假"函数，函数体写 `pass` 即可

**Q: 和 OpenAPI Webhooks 有什么区别？**
A: 回调挂在**具体接口**上（每个请求可能对应不同 URL）；Webhooks 是应用级的全局声明，URL 由应用配置决定（见下一章）

## 相关章节

- [28_OpenAPIWebhooks.md](./28_OpenAPIWebhooks.md) - OpenAPI Webhooks
- [06_OpenAPI额外响应.md](./06_OpenAPI额外响应.md) - 额外响应声明
- [02_路径操作高级配置.md](./02_路径操作高级配置.md) - 路径操作高级配置
