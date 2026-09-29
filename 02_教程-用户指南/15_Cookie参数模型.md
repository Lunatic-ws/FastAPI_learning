# 15 Cookie参数模型

## 学习目标

- 掌握如何使用Pydantic模型声明一组相关的Cookie参数
- 理解Cookie参数模型的优势和应用场景
- 学会禁止额外的Cookie参数

## 核心概念

当有一组相关的Cookie参数时，可以创建Pydantic模型来声明它们。这样可以：
- 在多个地方重用模型
- 一次性声明所有参数的验证和元数据

## 基本用法

### 使用Pydantic模型声明Cookie

```python
from typing import Annotated
from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

FastAPI会从请求的Cookie中提取每个字段的数据，并提供定义的Pydantic模型。

## 禁止额外Cookie

在某些特殊场景下，可能需要限制接收的Cookie参数：

```python
from typing import Annotated
from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    model_config = {"extra": "forbid"}
    
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

如果客户端尝试发送额外的Cookie，将收到错误响应：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please"
        }
    ]
}
```

## 文档说明

在 `/docs` API文档中可以看到定义的Cookie参数。

注意：浏览器以特殊方式处理Cookie，不允许JavaScript轻易接触它们。即使在文档UI中填写数据并点击"Execute"，由于文档UI使用JavaScript，Cookie不会被发送。

## 核心要点

1. **模型重用**：使用Pydantic模型可以在多个路径操作中重用Cookie参数定义
2. **统一验证**：可以一次性为所有参数声明验证规则
3. **禁止额外参数**：通过 `model_config = {"extra": "forbid"}` 可以拒绝额外的Cookie
4. **版本要求**：此功能从FastAPI 0.115.0版本开始支持
5. **适用范围**：同样的技术也适用于 `Query`、`Cookie` 和 `Header`

## 实际应用场景

- 用户会话管理
- 追踪和分析Cookie
- 多个相关Cookie参数的统一管理
- 需要严格控制Cookie参数的API

## 参考资源

- [FastAPI官方文档 - Cookie Parameter Models](https://fastapi.tiangolo.com/tutorial/cookie-param-models/)
