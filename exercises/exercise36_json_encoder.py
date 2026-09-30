# 练习36：JSON兼容编码器（JSON Compatible Encoder）
# 要求：根据注释要求实现相应的FastAPI应用
# 说明：从 fastapi.encoders 导入 jsonable_encoder
from datetime import datetime
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()
# 题目1：转换包含datetime的模型
# 创建Item模型: name(str), timestamp(datetime)
# 使用 jsonable_encoder(item) 将其转为JSON兼容的字典
# 打印结果，观察datetime被转成了什么格式

class Item(BaseModel):
    name: str
    timestamp: datetime


@app.post("/items/encoded")
def encode_item(item: Item) -> dict:
    encoded = jsonable_encoder(item)
    print(f"[jsonable_encoder] {encoded}")
    return encoded

# 题目2：转换非JSON原生类型
# 创建一个包含 bytes、set、UUID 的字典
# 使用 jsonable_encoder 转换，打印每个类型的转换结果

tricky_types = {
    "raw_bytes": b"FastAPI is great",
    "unique_tags": {"books", "authors", "users"},
    "request_id": UUID("12345678-1234-5678-1234-567812345678"),
}


@app.get("/types/encoded")
def encode_types() -> dict:
    encoded = jsonable_encoder(tricky_types)
    for key, value in encoded.items():
        print(f"[jsonable_encoder] {key} -> {value!r} ({type(value).__name__})")
    return encoded

# 题目3：存入模拟数据库
# 创建一个内存字典 fake_db = {}
# 用 jsonable_encoder 编码Item后以id为键存入
# 再从fake_db取出返回给客户端

fake_db: dict[int, dict] = {}
next_item_id = 1


@app.post("/db/items/")
def create_db_item(item: Item) -> dict:
    global next_item_id
    item_id = next_item_id
    next_item_id += 1
    fake_db[item_id] = jsonable_encoder(item)
    return {"id": item_id, "item": fake_db[item_id]}


@app.get("/db/items/{item_id}")
def read_db_item(item_id: int) -> dict:
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "item": fake_db[item_id]}

# 题目4：对比model_dump()
# 分别使用 item.model_dump() 和 jsonable_encoder(item)
# 构造一个包含datetime的Item，对比两者输出的差异
# 在注释中回答：为什么存入外部数据库前要用jsonable_encoder

def compare_model_dump_and_jsonable_encoder(item: Item) -> dict:
    """
    model_dump() 与 jsonable_encoder(item) 的差异:
    model_dump() 只在 Python 层做数据转换, datetime 仍然是 datetime 对象;
    jsonable_encoder(item) 会继续把 datetime 转成 ISO 8601 字符串, UUID 转成 str。

    为什么存入外部数据库前要用jsonable_encoder:
    外部数据库的驱动/存储层只认识 str、int、float、bool、None、list、dict 这些
    JSON 原生类型, 不认识 Python 原生的 datetime、UUID、Decimal 等对象。
    直接写 model_dump() 的结果会在写库时抛出 TypeError, 即使侥幸写入也无法保证
    读回来与原对象等价; jsonable_encoder 输出的值已经是可直接序列化/持久化的
    JSON 兼容数据, 所以入库前必须先经过它。
    """
    model_dump_result = item.model_dump()
    jsonable_encoder_result = jsonable_encoder(item)
    print(f"[model_dump] {model_dump_result}")
    print(f"[jsonable_encoder] {jsonable_encoder_result}")
    return {
        "item": item,
        "model_dump": {
            "name": model_dump_result["name"],
            "timestamp_repr": repr(model_dump_result["timestamp"]),
            "timestamp_type": type(model_dump_result["timestamp"]).__name__,
        },
        "jsonable_encoder": jsonable_encoder_result,
        "differs": model_dump_result != jsonable_encoder_result,
    }


@app.post("/items/compare")
def compare_encoders(item: Item) -> dict:
    return compare_model_dump_and_jsonable_encoder(item)

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
