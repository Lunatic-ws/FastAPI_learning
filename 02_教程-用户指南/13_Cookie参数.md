# 13 Cookie 参数

可以像定义 `Query` 和 `Path` 参数一样定义 Cookie 参数。

## 导入 Cookie

```python
from typing import Annotated
from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

## 声明 Cookie 参数

使用与 `Path` 和 `Query` 相同的结构声明 Cookie 参数：
- 定义默认值
- 添加验证或注解参数

```python
from typing import Annotated
from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

## 技术细节

- `Cookie` 是 `Path` 和 `Query` 的"姐妹"类，继承自相同的 `Param` 类
- 从 `fastapi` 导入的 `Query`、`Path`、`Cookie` 等实际上是返回特殊类的函数

## 重要说明

### 必须使用 Cookie
声明 Cookie 必须使用 `Cookie()`，否则参数会被解释为查询参数。

### 浏览器限制
- 浏览器以特殊方式处理 Cookie
- JavaScript 无法轻易操作 Cookie
- 在 `/docs` API 文档 UI 中可以看到 Cookie 文档
- 但由于文档 UI 使用 JavaScript，填写数据并点击"Execute"时，Cookie 不会被发送
- 会显示错误消息，如同未填写任何值

## 要点

1. 使用 `Cookie` 声明 Cookie 参数
2. 遵循与 `Query` 和 `Path` 相同的模式
3. Cookie 在浏览器中有特殊限制，测试时需注意
