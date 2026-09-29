# 16 Header参数模型

## 学习目标

- 掌握如何使用Pydantic模型声明一组相关的Header参数
- 理解Header参数模型的优势和应用场景
- 学会禁止额外的Header参数
- 了解下划线转换的处理方式

## 核心概念

当有一组相关的Header参数时，可以创建Pydantic模型来声明它们。这样可以：
- 在多个地方重用模型
- 一次性声明所有参数的验证和元数据

## 基本用法

### 使用Pydantic模型声明Header

```python
from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

FastAPI会从请求的Header中提取每个字段的数据，并提供定义的Pydantic模型。

## 禁止额外Header

在某些特殊场景下，可能需要限制接收的Header参数：

```python
from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}
    
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

如果客户端尝试发送额外的Header，将收到错误响应：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## 下划线转换处理

### 自动转换

默认情况下，参数名中的下划线会自动转换为连字符：
- 代码中的 `save_data` → HTTP Header的 `save-data`
- 在文档中也会显示为 `save-data`

### 禁用转换

如果需要禁用自动转换：

```python
from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(
    headers: Annotated[CommonHeaders, Header(convert_underscores=False)],
):
    return headers
```

警告：某些HTTP代理和服务器不允许使用带下划线的Header，禁用转换前请谨慎考虑。

## 文档说明

在 `/docs` API文档中可以看到定义的Header参数及其要求。

## 核心要点

1. **模型重用**：使用Pydantic模型可以在多个路径操作中重用Header参数定义
2. **统一验证**：可以一次性为所有参数声明验证规则
3. **禁止额外参数**：通过 `model_config = {"extra": "forbid"}` 可以拒绝额外的Header
4. **下划线转换**：默认将下划线转换为连字符，可通过 `convert_underscores=False` 禁用
5. **版本要求**：此功能从FastAPI 0.115.0版本开始支持

## 实际应用场景

- API认证和授权Header
- 追踪和监控Header（如分布式追踪）
- 缓存控制Header
- 自定义业务Header
- 需要严格控制Header参数的API

## 常见Header参数示例

```python
from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class AuthHeaders(BaseModel):
    authorization: str
    x_api_key: str
    x_request_id: str | None = None

@app.get("/protected/")
async def protected_route(headers: Annotated[AuthHeaders, Header()]):
    return {"api_key": headers.x_api_key}
```

## 参考资源

- [FastAPI官方文档 - Header Parameter Models](https://fastapi.tiangolo.com/tutorial/header-param-models/)
