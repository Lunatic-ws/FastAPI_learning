# 06 OpenAPI中的额外响应 (Additional Responses in OpenAPI)

## 概述

可以声明额外响应，包含额外的状态码、媒体类型、描述等。

这些额外响应将包含在OpenAPI模式中，也会出现在API文档中。

但对于这些额外响应，必须确保直接返回`Response`（如`JSONResponse`），并带有状态码和内容。

## 带model的额外响应

可以向路径操作装饰器传递`responses`参数。

它接收一个`dict`：键是每个响应的状态码（如`200`），值是包含每个响应信息的其他`dict`。

每个响应`dict`可以有一个`model`键，包含Pydantic模型，就像`response_model`。

### 示例

声明另一个状态码`404`和Pydantic模型`Message`的响应：

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

class Message(BaseModel):
    message: str

app = Flask()

@app.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    return JSONResponse(status_code=404, content={"message": "Item not found"})
```

### 重要说明

- 必须直接返回`JSONResponse`
- `model`键不是OpenAPI的一部分
- FastAPI会从那里获取Pydantic模型，生成JSON Schema，放在正确位置

## 主响应的其他媒体类型

可以使用相同的`responses`参数为主响应添加不同的媒体类型。

例如，添加`image/png`媒体类型，声明路径操作可以返回JSON对象（媒体类型`application/json`）或PNG图像：

```python
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

app = FastAPI()

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
async def read_item(item_id: str, img: bool | None = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}
```

## 组合信息

可以组合来自多个地方的响应信息，包括`response_model`、`status_code`和`responses`参数。

可以声明`response_model`，使用默认状态码`200`（或自定义），然后在`responses`中为该响应声明额外信息。

FastAPI会保留`responses`中的额外信息，并与模型的JSON Schema组合。

### 示例

声明状态码`404`使用Pydantic模型并具有自定义`description`，以及状态码`200`使用`response_model`但包含自定义`example`：

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

class Message(BaseModel):
    message: str

app = FastAPI()

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"}
                }
            },
        },
    },
)
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
```

## 组合预定义响应和自定义响应

可能希望有一些适用于多个路径操作的预定义响应，但又想将它们与每个路径操作所需的自定义响应组合。

可以使用Python的"解包"技术，用`**dict_to_unpack`：

```python
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

app = FastAPI()

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={**responses, 200: {"content": {"image/png": {}}}},
)
async def read_item(item_id: str, img: bool | None = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}
```

## 关键点

1. **responses参数**：声明额外状态码和响应
2. **model键**：指定Pydantic模型用于生成JSON Schema
3. **媒体类型**：可以声明多种媒体类型
4. **组合信息**：response_model、status_code、responses可以组合
5. **预定义响应**：使用`**dict`解包技术重用响应定义
6. **OpenAPI文档**：额外响应会自动出现在API文档中

## 更多信息

查看OpenAPI规范：
- [OpenAPI Responses Object](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#responses-object)
- [OpenAPI Response Object](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#response-object)
