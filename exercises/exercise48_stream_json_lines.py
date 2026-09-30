# 练习48：流式JSON行
#
# 目标：使用生成器流式传输JSON数据
#
# 任务：
# 1. 定义一个Pydantic模型 Item(name: str, price: float)
# 2. 创建一个 GET /items/stream 端点
# 3. 使用 yield 流式返回多个Item对象
# 4. 设置返回类型为 AsyncIterable[Item]
#
# 提示：
# - 导入 from collections.abc import AsyncIterable
# - 使用 yield 而非 return
# - 每个yield生成一个Item对象
# - 客户端接收到的是JSON Lines格式

import asyncio
from collections.abc import AsyncIterable

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


catalog: list[Item] = [
    Item(name="Hammer", price=9.99),
    Item(name="Nail", price=0.5),
    Item(name="Screw", price=1.25),
    Item(name="Wrench", price=15.0),
    Item(name="Drill", price=49.9),
]


@app.get("/items/stream")
async def stream_items() -> AsyncIterable[Item]:
    for item in catalog:
        await asyncio.sleep(0.01)
        yield item

if __name__ == "__main__":
    pass
