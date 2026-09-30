# 04 直接返回Response (Return a Response Directly)

## 概述

创建FastAPI路径操作时，通常可以返回任何数据：`dict`、`list`、Pydantic模型、数据库模型等。

如果声明了响应模型，FastAPI会使用Pydantic将其序列化为JSON。

如果未声明响应模型，FastAPI会使用`jsonable_encoder`并将其放入`JSONResponse`。

你也可以直接创建并返回`JSONResponse`。

## 返回Response

你可以返回`Response`或其任何子类。

当返回`Response`时，FastAPI会直接传递它：
- 不会用Pydantic模型进行数据转换
- 不会将内容转换为任何类型
- 这提供了很大的灵活性
- 但也带来了责任：必须确保返回的数据正确、格式正确、可序列化等

## 在Response中使用jsonable_encoder

因为FastAPI不会修改你返回的`Response`，必须确保其内容已准备好。

例如，不能直接将Pydantic模型放入`JSONResponse`，而不先将其转换为`dict`，并将所有数据类型（如`datetime`、`UUID`等）转换为JSON兼容类型。

对于这些情况，可以使用`jsonable_encoder`在传递给响应之前转换数据：

```python
from datetime import datetime
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

app = FastAPI()

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)
```

## 返回自定义Response

上述示例展示了所有需要的部分，但不太有用，因为可以直接返回`item`，FastAPI会将其放入`JSONResponse`，转换为`dict`等。

现在看看如何用它返回自定义响应。

### 返回XML响应

假设你想返回XML响应：

```python
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")
```

## 响应模型如何工作

在路径操作中声明响应模型时，FastAPI会使用Pydantic将其序列化为JSON：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
```

这将在Rust端进行，性能比使用常规Python和`JSONResponse`类好得多。

使用`response_model`或返回类型时，FastAPI不会使用`jsonable_encoder`转换数据（这会更慢），也不会使用`JSONResponse`类。

相反，它获取Pydantic使用响应模型（或返回类型）生成的JSON字节，并直接返回具有正确JSON媒体类型的`Response`（`application/json`）。

## 注意事项

直接返回`Response`时：
- 其数据不会自动验证、转换（序列化）或记录
- 但仍可使用额外响应在OpenAPI中记录

## 关键点

1. **灵活性**：直接返回Response可以完全控制响应
2. **责任**：需要自己确保数据格式正确
3. **性能**：使用响应模型比直接返回JSONResponse性能更好
4. **转换工具**：使用`jsonable_encoder`转换复杂数据类型
5. **自定义格式**：可以返回XML、HTML等任何格式
