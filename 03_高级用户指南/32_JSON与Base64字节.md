# 32 JSON与Base64字节

## 学习目标

- 理解 JSON 无法直接承载二进制数据的原因
- 掌握 Pydantic 的 `val_json_bytes` / `ser_json_bytes` 以 Base64 处理 bytes 字段

## 核心概念

### 1. 优先考虑文件而不是 Base64

JSON 只能包含 UTF-8 字符串，无法直接包含原始字节。二进制数据的更好选择：

- **上传**：请求文件（multipart/form-data）
- **下载**：FileResponse / 自定义二进制响应

Base64 会把数据膨胀约 1/3（4 字符表示 3 字节），比文件传输效率低。**仅当确实需要在 JSON 中嵌入二进制且无法用文件时才用 Base64。**

### 2. 输入：val_json_bytes

声明 `bytes` 字段 + 模型配置 `val_json_bytes: "base64"`，Pydantic 在验证 JSON 时自动把 Base64 字符串**解码**为字节：

```python
from fastapi import FastAPI
from pydantic import BaseModel

class DataInput(BaseModel):
    description: str
    data: bytes

    model_config = {"val_json_bytes": "base64"}

app = FastAPI()

@app.post("/data")
def post_data(body: DataInput):
    content = body.data.decode("utf-8")
    return {"description": body.description, "content": content}
```

请求体：

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

- `aGVsbG8=` 是 `hello` 的 Base64 编码
- 模型内拿到的 `body.data` 已是原始 `bytes`，可直接按字节处理
- `/docs` 中该字段会标注为 Base64 编码的字节

### 3. 输出：ser_json_bytes

`ser_json_bytes: "base64"` 让 Pydantic 序列化响应时把字节**编码**为 Base64 字符串：

```python
class DataOutput(BaseModel):
    description: str
    data: bytes

    model_config = {"ser_json_bytes": "base64"}

@app.get("/data")
def get_data() -> DataOutput:
    data = "hello".encode("utf-8")
    return DataOutput(description="A plumbus", data=data)
```

响应中 `data` 即为 `"aGVsbG8="`。

### 4. 输入输出共用同一模型

```python
class DataInputOutput(BaseModel):
    description: str
    data: bytes

    model_config = {
        "val_json_bytes": "base64",
        "ser_json_bytes": "base64",
    }

@app.post("/data-in-out")
def post_data_in_out(body: DataInputOutput) -> DataInputOutput:
    return body
```

## 最佳实践

1. **先问能不能用文件**：大体积二进制走 multipart 上传和 FileResponse 下载
2. **输入输出模型分开**：`DataInput` / `DataOutput` 各配各的 config，需求不同时不强行共用
3. **Base64 只在 JSON 生态内闭环**：对方系统只收 JSON 时才用它

## 常见问题

**Q: 不配置 val_json_bytes 直接传 bytes 字段会怎样？**
A: 默认模式是 "utf8"，Pydantic 会把 JSON 字符串按 UTF-8 解码为 bytes，无法处理任意二进制（非法 UTF-8 直接报错）

**Q: Base64 传输的体积膨胀多少？**
A: 约 33%；大文件场景差距会非常明显

## 相关章节

- [22_请求文件.md](../02_教程-用户指南/22_请求文件.md) - 请求文件上传
- [05_自定义Response.md](./05_自定义Response.md) - FileResponse 等自定义响应
- [10_嵌套模型.md](../02_教程-用户指南/10_嵌套模型.md) - Pydantic 模型
