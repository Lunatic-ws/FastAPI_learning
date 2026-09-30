# 07 响应Cookie

## 学习目标

- 掌握在响应中设置与删除 Cookie
- 了解 Cookie 的安全参数（httponly、secure、samesite 等）

## 核心概念

### 1. 注入 Response 参数

声明 `Response` 类型参数，FastAPI 会传递响应对象，你可以在其上设置 Cookie：

```python
from fastapi import FastAPI, Response

app = FastAPI()

@app.post("/cookie/")
async def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}
```

- 还可以正常返回字典/对象等响应内容，FastAPI 会把 Cookie 合并进最终响应
- 也可声明为 `Annotated[str, Cookie()]` 读取请求中的 Cookie

### 2. set_cookie 的完整参数

```python
response.set_cookie(
    key="session",
    value="abc123",
    max_age=3600,          # 秒为单位的存活时间
    expires=None,          # 过期时间戳
    path="/",
    domain=None,
    secure=True,           # 仅 HTTPS 传输
    httponly=True,         # JS 无法读取（防 XSS 窃取）
    samesite="lax",        # 防 CSRF：lax / strict / none
)
```

### 3. 删除 Cookie

```python
@app.post("/logout/")
async def logout(response: Response):
    response.delete_cookie(key="session")
    return {"message": "已退出"}
```

### 4. 直接返回 Response 时设置

不使用 `response` 参数注入时，也可以直接构造响应并设置 Cookie：

```python
from fastapi.responses import JSONResponse

@app.get("/direct/")
async def direct():
    content = {"message": "hello"}
    response = JSONResponse(content=content)
    response.set_cookie(key="token", value="xyz")
    return response
```

## 最佳实践

1. **会话类 Cookie 加 httponly + secure + samesite**：三者配合抵御 XSS 窃取与 CSRF
2. **注入 Response 参数更简洁**：比手动构造 JSONResponse 的侵入性小
3. **令牌不要放 Cookie 明文**：配合 JWT 时注意签名校验

## 常见问题

**Q: 设置了 Cookie 但浏览器没收到？**
A: 检查是不是通过 `return` 直接返回了新 Response 对象而没有带上 Cookie；跨域场景还需 CORS 配置 `allow_credentials=True` 且前端 `credentials: "include"`

**Q: set_cookie 和 delete_cookie 的 path 要一致吗？**
A: 是的，path/domain 不一致时删除的是另一个 Cookie

## 相关章节

- [08_响应Headers.md](./08_响应Headers.md) - 响应头设置
- [03_额外状态码.md](./03_额外状态码.md) - 额外状态码
- [09_响应更改状态码.md](./09_响应更改状态码.md) - 响应更改状态码
