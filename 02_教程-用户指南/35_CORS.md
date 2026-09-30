# 35 CORS（跨域资源共享）

CORS或"Cross-Origin Resource Sharing"指的是当前端（运行在浏览器中）的JavaScript代码与后端通信，而后端位于不同的"源"（origin）的情况。

## 14.1 什么是源（Origin）

源是协议（`http`、`https`）、域名（`myapp.com`、`localhost`）和端口（`80`、`443`、`8080`）的组合。

例如，这些都是不同的源：
- `http://localhost`
- `https://localhost`
- `http://localhost:8080`

即使都在`localhost`，但使用不同的协议或端口，所以它们是不同的"源"。

## 14.2 CORS工作流程

假设前端运行在`http://localhost:8080`，JavaScript尝试与运行在`http://localhost`的后端通信（默认端口80）。

浏览器会：
1. 发送HTTP `OPTIONS`请求到后端
2. 后端发送适当的头部授权来自`http://localhost:8080`的通信
3. 浏览器允许前端JavaScript发送请求到后端

## 14.3 使用CORSMiddleware

在FastAPI中配置CORS：

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许的源列表
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}
```

## 14.4 CORSMiddleware参数

- `allow_origins`：允许跨域请求的源列表。例如`['https://example.org']`。使用`['*']`允许所有源。
- `allow_origin_regex`：匹配允许源的正则表达式字符串。例如`'https://.*\.example\.org'`。
- `allow_methods`：允许的HTTP方法列表。默认`['GET']`。使用`['*']`允许所有标准方法。
- `allow_headers`：支持的HTTP请求头部列表。默认`[]`。使用`['*']`允许所有头部。
- `allow_credentials`：是否支持跨域请求中的Cookie。默认`False`。
  - 如果设置为`True`，`allow_origins`、`allow_methods`和`allow_headers`不能使用`['*']`，必须显式指定。
- `expose_headers`：浏览器可访问的响应头部列表。默认`[]`。
- `max_age`：浏览器缓存CORS响应的最大时间（秒）。默认`600`。

## 14.5 通配符的限制

使用`"*"`通配符可以允许所有源，但会限制某些类型的通信，特别是涉及凭证（Cookies、Authorization头部等）的请求。

因此，为了所有功能正常工作，最好显式指定允许的源。

## 14.6 CORS预检请求

中间件响应两种特定类型的HTTP请求：

### 预检请求（Preflight）
任何带有`Origin`和`Access-Control-Request-Method`头部的`OPTIONS`请求。

中间件拦截请求并返回适当的CORS头部，状态码为`200`或`400`。

### 简单请求（Simple Requests）
任何带有`Origin`头部的请求。

中间件将请求传递给应用，但在响应中包含适当的CORS头部。

## 小结

- CORS用于处理跨源通信
- 源由协议、域名和端口组成
- 使用`CORSMiddleware`配置CORS
- 可以指定允许的源、方法、头部等
- 涉及凭证时不能使用通配符`"*"`
- 最好显式指定允许的源以确保所有功能正常

下一节将学习依赖注入系统。
