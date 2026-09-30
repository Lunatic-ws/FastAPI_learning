# 05 自定义Response - HTML, Stream, File等 (Custom Response)

## 概述

默认情况下，FastAPI会返回JSON响应。

可以通过直接返回`Response`来覆盖它。

但如果直接返回`Response`（或任何子类，如`JSONResponse`），数据不会被自动转换，文档也不会自动生成。

不过，也可以在路径操作装饰器中使用`response_class`参数声明要使用的`Response`。

## JSON响应

### 默认行为

默认FastAPI返回JSON响应：
- 如果声明响应模型，FastAPI会使用Pydantic将其序列化为JSON
- 如果不声明响应模型，FastAPI会使用`jsonable_encoder`并将其放入`JSONResponse`

### JSON性能

**重要**：如果想要最大性能，使用响应模型，不要在路径操作装饰器中声明`response_class`。

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
```

## HTML响应

要直接从FastAPI返回HTML响应，使用`HTMLResponse`：

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
```

`response_class`参数将用于定义响应的"媒体类型"（HTTP头`Content-Type`设置为`text/html`）。

## 可用的响应类型

### Response

主`Response`类，所有其他响应继承自它。

参数：
- `content` - `str`或`bytes`
- `status_code` - `int` HTTP状态码
- `headers` - `dict`字符串
- `media_type` - `str`媒体类型，如`"text/html"`

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

### HTMLResponse

接受文本或字节并返回HTML响应。

### PlainTextResponse

接受文本或字节并返回纯文本响应。

```python
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello World"
```

### JSONResponse

接受数据并返回`application/json`编码响应。

这是FastAPI中使用的默认响应。

### RedirectResponse

返回HTTP重定向。默认使用307状态码（临时重定向）。

直接返回：

```python
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")
```

或在`response_class`参数中使用：

```python
@app.get("/fastapi", response_class=RedirectResponse)
async def redirect_fastapi():
    return "https://fastapi.tiangolo.com"
```

### StreamingResponse

接受异步生成器或普通生成器/迭代器（带`yield`的函数）并流式传输响应体。

```python
import anyio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"
        await anyio.sleep(0)

@app.get("/")
async def main():
    return StreamingResponse(fake_video_streamer())
```

### FileResponse

异步流式传输文件作为响应。

参数：
- `path` - 要流式传输的文件路径
- `headers` - 要包含的任何自定义头
- `media_type` - 媒体类型字符串
- `filename` - 如果设置，将包含在响应`Content-Disposition`中

```python
from fastapi import FastAPI
from fastapi.responses import FileResponse

some_file_path = "large-video-file.mp4"

app = FastAPI()

@app.get("/")
async def main():
    return FileResponse(some_file_path)
```

## 自定义响应类

可以创建自定义响应类，继承自`Response`：

```python
from typing import Any
import orjson
from fastapi import FastAPI, Response

app = FastAPI()

class CustomORJSONResponse(Response):
    media_type = "application/json"
    
    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)

@app.get("/", response_class=CustomORJSONResponse)
async def main():
    return {"message": "Hello World"}
```

### orjson或响应模型

如果追求性能，使用响应模型可能比`orjson`响应更好。

响应模型下，FastAPI使用Pydantic直接序列化数据为JSON，不使用中间步骤。

Pydantic底层使用与`orjson`相同的Rust机制序列化JSON，因此使用响应模型已经可以获得最佳性能。

## 默认响应类

创建FastAPI实例或APIRouter时，可以指定默认使用的响应类：

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(default_response_class=HTMLResponse)

@app.get("/items/")
async def read_items():
    return "<h1>Items</h1><p>This is a list of items.</p>"
```

## 关键点

1. **response_class参数**：声明响应类型，自动设置Content-Type
2. **直接返回Response**：覆盖默认行为，但不会自动生成文档
3. **性能考虑**：响应模型 > JSONResponse > 自定义响应
4. **多种响应类型**：HTML、文本、重定向、流、文件等
5. **自定义响应类**：继承Response并实现render方法
