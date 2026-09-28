# 14 Header 参数

可以像定义 `Query`、`Path` 和 `Cookie` 参数一样定义 Header 参数。

## 导入 Header

```python
from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

## 声明 Header 参数

使用与 `Path`、`Query` 和 `Cookie` 相同的结构声明 Header 参数：
- 定义默认值
- 添加验证或注解参数

## 自动转换

`Header` 提供了额外的功能：

### 下划线转连字符
- 大多数标准 header 用连字符（`-`）分隔
- `user-agent` 这样的变量名在 Python 中无效
- 默认情况下，`Header` 会将参数名的下划线（`_`）转换为连字符（`-`）

### 大小写不敏感
- HTTP headers 大小写不敏感
- 可使用标准 Python 风格（snake_case）
- 可使用 `user_agent` 而非 `User_Agent`

### 禁用自动转换
```python
@app.get("/items/")
async def read_items(
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None,
):
    return {"strange_header": strange_header}
```

**警告**：某些 HTTP 代理和服务器不允许使用带下划线的 header。

## 重复 Header

可以接收重复的 header（相同 header 有多个值）：

```python
@app.get("/items/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}
```

发送两个 HTTP headers：
```
X-Token: foo
X-Token: bar
```

响应：
```json
{
    "X-Token values": ["bar", "foo"]
}
```

## 技术细节

- `Header` 是 `Path`、`Query` 和 `Cookie` 的"姐妹"类，继承自相同的 `Param` 类
- 从 `fastapi` 导入的这些实际上是返回特殊类的函数

## 重要说明

声明 header 必须使用 `Header()`，否则参数会被解释为查询参数。

## 要点

1. 使用 `Header` 声明 header 参数
2. 遵循与 `Query`、`Path` 和 `Cookie` 相同的模式
3. 无需担心变量名中的下划线，FastAPI 会自动转换
4. 可使用 `list` 类型接收重复的 header
