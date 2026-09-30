# 26 JSON编码器 (JSON Compatible Encoder)

## 学习目标

学习如何使用 FastAPI 的 `jsonable_encoder` 函数将数据类型转换为 JSON 兼容格式。

## 为什么需要 JSON 编码器

在某些情况下，你可能需要将数据类型（如 Pydantic 模型）转换为与 JSON 兼容的内容（如 `dict`、`list` 等）。

例如，如果需要将其存储在数据库中：
- 数据库不接收 `datetime` 对象，需要转换为 ISO 格式的字符串
- 数据库不接收 Pydantic 模型，需要转换为字典

## 使用 jsonable_encoder

假设你有一个数据库 `fake_db`，只接收 JSON 兼容数据：

```python
from datetime import datetime
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
```

在这个例子中，它会将 Pydantic 模型转换为 `dict`，将 `datetime` 转换为 `str`。

## 转换示例

### 基本转换

```python
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class User(BaseModel):
    name: str
    created_at: datetime
    age: int


user = User(name="Alice", created_at=datetime.now(), age=30)
json_data = jsonable_encoder(user)

print(json_data)
# 输出: {'name': 'Alice', 'created_at': '2024-01-15T10:30:00', 'age': 30}
```

### 包含嵌套模型

```python
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str


class User(BaseModel):
    name: str
    address: Address
    created_at: datetime


user = User(
    name="Bob",
    address=Address(street="123 Main St", city="NYC"),
    created_at=datetime.now()
)
json_data = jsonable_encoder(user)

print(json_data)
# 输出: {
#     'name': 'Bob',
#     'address': {'street': '123 Main St', 'city': 'NYC'},
#     'created_at': '2024-01-15T10:30:00'
# }
```

### 包含列表和集合

```python
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class Item(BaseModel):
    tags: set[str]
    created_at: datetime


item = Item(tags={"python", "fastapi", "web"}, created_at=datetime.now())
json_data = jsonable_encoder(item)

print(json_data)
# 输出: {'tags': ['python', 'fastapi', 'web'], 'created_at': '2024-01-15T10:30:00'}
# 注意：set 被转换为 list
```

## 返回值说明

调用 `jsonable_encoder` 的结果是：
- 一个 Python 标准数据结构（如 `dict`）
- 所有值和子值都与 JSON 兼容
- 可以用 Python 标准的 `json.dumps()` 编码

它**不**返回包含 JSON 格式数据的大型字符串，而是返回一个标准数据结构。

## 内部使用

`jsonable_encoder` 实际上被 FastAPI 内部用于转换数据。但它在许多其他场景中也很有用：

- 存储数据到数据库
- 日志记录
- 缓存数据
- 与其他需要 JSON 数据的系统交互

## 完整应用示例

```python
from datetime import datetime
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    created_at: datetime


fake_db = {}


@app.post("/items/{item_id}")
async def create_item(item_id: str, item: Item):
    # 转换为 JSON 兼容格式
    json_compatible_item_data = jsonable_encoder(item)
    
    # 存储到数据库
    fake_db[item_id] = json_compatible_item_data
    
    # 也可以直接用 json.dumps 序列化
    json_string = json.dumps(json_compatible_item_data)
    
    return {
        "item_id": item_id,
        "stored_data": json_compatible_item_data,
        "json_string": json_string
    }


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return fake_db.get(item_id, {"error": "Item not found"})
```

## 核心要点

1. `jsonable_encoder` 将数据转换为 JSON 兼容格式
2. 自动处理 `datetime`、Pydantic 模型等特殊类型
3. 返回标准 Python 数据结构，不是 JSON 字符串
4. 可用于数据库存储、日志、缓存等场景
5. FastAPI 内部也使用此函数

## 实际应用场景

- 存储数据到 NoSQL 数据库
- Redis 缓存数据
- 日志记录复杂对象
- 与外部 API 交互
- 生成 JSON 响应

## 练习

创建一个包含 `datetime` 字段、嵌套模型和列表的复杂模型，使用 `jsonable_encoder` 转换并查看结果。
