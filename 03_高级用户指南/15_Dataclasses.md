# 15 使用Dataclasses

## 概述

FastAPI基于Pydantic,通常使用Pydantic模型声明请求和响应。但FastAPI也支持使用Python标准库的`dataclasses`,使用方式与Pydantic模型类似。

## 基本用法

```python
from dataclasses import dataclass
from fastapi import FastAPI

@dataclass
class Item:
    name: str
    price: float
    description: str | None = None
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

## 工作原理

Pydantic内部支持标准dataclasses,会将其转换为Pydantic风格的dataclass。因此支持:

- 数据验证
- 数据序列化
- 数据文档生成

**注意**: dataclasses不能做Pydantic模型能做的所有事情,某些高级功能仍需Pydantic模型。

## 在response_model中使用

```python
from dataclasses import dataclass, field
from fastapi import FastAPI

@dataclass
class Item:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    description: str | None = None
    tax: float | None = None

app = FastAPI()

@app.get("/items/next", response_model=Item)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be playin' and havin' fun",
        "tags": ["breater"],
    }
```

dataclass会自动转换为Pydantic dataclass,其schema会出现在API文档UI中。

## 嵌套数据结构

可以组合dataclasses和其他类型注解形成嵌套数据结构:

```python
from dataclasses import field
from fastapi import FastAPI
from pydantic.dataclasses import dataclass

@dataclass
class Item:
    name: str
    description: str | None = None

@dataclass
class Author:
    name: str
    items: list[Item] = field(default_factory=list)

app = FastAPI()

@app.post("/authors/{author_id}/items/", response_model=Author)
async def create_author_items(author_id: str, items: list[Item]):
    return {"name": author_id, "items": items}

@app.get("/authors/", response_model=list[Author])
def get_authors():
    return [
        {
            "name": "Breaters",
            "items": [
                {
                    "name": "Island In The Moon",
                    "description": "A place to be playin' and havin' fun",
                },
                {"name": "Holy Buddies"},
            ],
        },
        {
            "name": "System of an Up",
            "items": [
                {
                    "name": "Salt",
                    "description": "The kombucha mushroom people's favorite",
                },
                {"name": "Pad Thai"},
            ],
        },
    ]
```

### 使用Pydantic dataclasses

有时可能需要使用Pydantic版本的dataclasses,例如自动生成的API文档有问题时。可以直接替换:

```python
from dataclasses import field
from fastapi import FastAPI
from pydantic.dataclasses import dataclass  # 使用Pydantic的dataclass
```

`pydantic.dataclasses`是标准dataclasses的替代品,可以无缝切换。

## 与Pydantic模型混合使用

dataclasses可以与Pydantic模型组合使用:

- 继承Pydantic模型
- 在模型中包含dataclasses
- 在dataclasses中包含Pydantic模型

## 优势与限制

### 优势
- 可以复用现有dataclasses
- 学习曲线更平缓
- 与标准库兼容性好

### 限制
- 不支持所有Pydantic功能
- 验证能力有限
- 某些高级类型转换不支持

## 版本要求

此功能自FastAPI 0.67.0起可用。

## 小结

- FastAPI支持使用标准dataclasses声明请求/响应
- Pydantic会自动转换并支持验证、序列化、文档
- 可以在response_model中使用
- 可以组合形成嵌套结构
- 某些场景需使用`pydantic.dataclasses`
- 适合复用现有dataclasses的场景
