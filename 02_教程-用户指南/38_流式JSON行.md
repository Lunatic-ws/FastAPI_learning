# 38 流式JSON行

使用生成器流式传输JSON数据，适用于AI LLM服务、日志、遥测等场景。

## 安装

```bash
pip install fastapi uvicorn
```

## 什么是流式传输？

流式传输（Streaming）指应用开始发送数据项给客户端，无需等待整个序列准备完毕。

客户端接收并处理第一个数据项时，服务端可能还在生产下一个数据项。

## JSON Lines格式

JSON Lines是一种格式，每行一个JSON对象。

响应Content-Type为`application/jsonl`（而非`application/json`），内容示例：

```
{"name": "Plumbus", "description": "A multi-purpose household device."}
{"name": "Portal Gun", "description": "A portal opening device."}
{"name": "Meeseeks Box", "description": "A box that summons a Meeseeks."}
```

类似JSON数组，但每行一个JSON对象，用换行符分隔。

## 流式JSON行示例

```python
from collections.abc import AsyncIterable
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None

items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]

@app.get("/items/stream")
async def stream_items() -> AsyncIterable[Item]:
    for item in items:
        yield item
```

## 非异步函数

```python
from collections.abc import Iterable

@app.get("/items/stream-no-async")
def stream_items_no_async() -> Iterable[Item]:
    for item in items:
        yield item
```

FastAPI确保非async函数正确运行，不阻塞事件循环。

## 无返回类型注解

```python
@app.get("/items/stream-no-annotation")
async def stream_items_no_annotation():
    for item in items:
        yield item
```

FastAPI使用`jsonable_encoder`转换数据并序列化为JSON Lines。

## 运行

```bash
uvicorn main:app --reload
```

## 访问

- http://127.0.0.1:8000/items/stream - 流式JSON行响应
- http://127.0.0.1:8000/docs - 自动文档

## 核心要点

- `yield`生成数据项，而非`return`
- 异步函数返回类型：`AsyncIterable[Model]`
- 非异步函数返回类型：`Iterable[Model]`
- Pydantic序列化在Rust端，性能高
- 每个JSON对象用换行符分隔
- 适用于AI LLM、日志、遥测等流式场景
