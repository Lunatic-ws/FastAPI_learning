# 14 直接使用Request对象

## 概述

到目前为止,我们一直通过类型注解来声明请求的各个部分,FastAPI会自动验证、转换数据并生成文档。但有时我们需要直接访问Request对象本身。

## Request对象详情

FastAPI底层是Starlette,因此可以直接使用Starlette的Request对象。

**注意**: 如果直接从Request对象获取数据(例如读取body),FastAPI不会对该数据进行验证、转换或生成文档。

## 使用Request对象

### 基本示例

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}
```

通过将路径操作函数参数类型声明为Request,FastAPI会自动传入Request对象。

### 常用Request属性

- `request.client.host` - 客户端IP地址
- `request.url` - 请求URL
- `request.method` - HTTP方法
- `request.headers` - 请求头
- `request.query_params` - 查询参数
- `request.path_params` - 路径参数
- `request.cookies` - Cookies
- `request.session` - Session(需配合中间件)

### 异步读取body

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/items/")
async def create_item(request: Request):
    body = await request.json()
    return body
```

## 混合使用

可以同时使用常规参数和Request对象:

```python
from fastapi import FastAPI, Request
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Item, request: Request):
    client_host = request.client.host
    return {
        "item_id": item_id,
        "item": item,
        "client_host": client_host
    }
```

## 什么时候使用Request对象

1. 需要获取客户端IP地址
2. 需要访问原始请求头
3. 需要处理非标准格式的请求体
4. 需要实现自定义认证逻辑
5. 需要访问底层的Starlette功能

## 相关文档

- [Starlette Request文档](https://starlette.dev/requests/)
- [FastAPI Request参考](https://fastapi.tiangolo.com/reference/request/)

## 小结

- 可以通过类型注解Request直接访问请求对象
- 直接使用Request时数据不会被验证和转换
- 可以混合使用常规参数和Request对象
- 适用于需要访问底层请求信息的场景
