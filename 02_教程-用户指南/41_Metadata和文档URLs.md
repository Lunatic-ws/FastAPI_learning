# 41 Metadata和文档URLs（Metadata and Docs URLs）

## 核心概念

可以为FastAPI应用设置多种元数据配置，用于OpenAPI规范和自动生成的API文档界面。

### API元数据

在创建FastAPI实例时设置以下字段：

```python
from fastapi import FastAPI

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]
```

#### 可设置的元数据字段

| 参数 | 类型 | 描述 |
|------|------|------|
| `title` | `str` | API标题 |
| `summary` | `str` | API简短摘要（OpenAPI 3.1.0+） |
| `description` | `str` | API描述（支持Markdown） |
| `version` | `str` | API版本（应用自己的版本） |
| `terms_of_service` | `str` | 服务条款URL |
| `contact` | `dict` | 联系信息 |
| `license_info` | `dict` | 许可证信息 |

#### contact字段

```python
contact={
    "name": "联系名称",
    "url": "联系URL",
    "email": "邮箱地址"
}
```

#### license_info字段

```python
# 方式1：使用URL
license_info={
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
}

# 方式2：使用SPDX标识符（OpenAPI 3.1.0+）
license_info={
    "name": "Apache 2.0",
    "identifier": "Apache-2.0",
}
```

### 标签元数据

使用`openapi_tags`参数为不同标签添加元数据：

```python
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]

@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]
```

#### 标签元数据字段

每个标签字典可包含：

- `name`（必需）：标签名称
- `description`：标签描述（支持Markdown）
- `externalDocs`：外部文档
  - `description`：外部文档描述
  - `url`（必需）：外部文档URL

**注意**：标签元数据字典的顺序决定了文档UI中的显示顺序。

### OpenAPI URL

默认OpenAPI schema在`/openapi.json`，可以自定义：

```python
from fastapi import FastAPI

# 自定义OpenAPI URL
app = FastAPI(openapi_url="/api/v1/openapi.json")

# 禁用OpenAPI schema和文档界面
# app = FastAPI(openapi_url=None)

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
```

### 文档URLs

配置两个文档界面：

```python
from fastapi import FastAPI

# 自定义Swagger UI URL，禁用ReDoc
app = FastAPI(
    docs_url="/documentation",  # Swagger UI从/documentation访问
    redoc_url=None  # 禁用ReDoc
)

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
```

#### 默认路径

- **Swagger UI**：`/docs`
  - 自定义：`docs_url="/custom-docs"`
  - 禁用：`docs_url=None`
  
- **ReDoc**：`/redoc`
  - 自定义：`redoc_url="/custom-redoc"`
  - 禁用：`redoc_url=None`

## 关键要点

1. **description支持Markdown**：可以使用Markdown语法丰富API文档描述
2. **标签顺序**：`openapi_tags`列表中的顺序决定文档UI显示顺序
3. **完全禁用文档**：设置`openapi_url=None`可禁用OpenAPI schema和所有文档界面
4. **版本信息**：`version`参数是应用自己的版本，不是OpenAPI版本

## 实际应用场景

### 1. 企业级API文档

```python
app = FastAPI(
    title="企业API",
    description="""
    # 概述
    
    这是企业级RESTful API。
    
    ## 认证
    
    使用Bearer Token认证。
    
    ## 限流
    
    每分钟最多100次请求。
    """,
    version="2.1.0",
    contact={
        "name": "API支持团队",
        "email": "api-support@company.com",
    },
)
```

### 2. 开源项目API

```python
app = FastAPI(
    title="MyOpenSource API",
    version="1.0.0",
    license_info={
        "name": "MIT",
        "identifier": "MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)
```

### 3. 微服务API

```python
app = FastAPI(
    title="用户服务",
    description="用户管理微服务API",
    version="1.0.0",
    openapi_url="/user-service/openapi.json",
    docs_url="/user-service/docs",
)
```
