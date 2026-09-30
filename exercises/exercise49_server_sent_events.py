# 练习49：服务器发送事件（SSE）
#
# 目标：使用SSE流式传输数据到客户端
#
# 任务：
# 1. 导入 EventSourceResponse 和 ServerSentEvent
# 2. 创建 GET /stream 端点，设置 response_class=EventSourceResponse
# 3. 使用 yield ServerSentEvent(data=item) 发送事件
# 4. 实现一个断点续传功能，读取 Last-Event-ID 头
#
# 提示：
# - 导入 from fastapi.sse import EventSourceResponse, ServerSentEvent
# - ServerSentEvent可设置 data, event, id, retry, comment 字段
# - 使用 raw_data 发送未经JSON编码的原始文本
# - 浏览器通过 EventSource API 接收SSE
import asyncio
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.responses import StreamingResponse
from fastapi.sse import EventSourceResponse, ServerSentEvent

app = FastAPI()

events: list[dict[str, object]] = [
    {"id": 1, "message": "服务器已启动", "progress": 0},
    {"id": 2, "message": "正在处理任务", "progress": 50},
    {"id": 3, "message": "任务完成", "progress": 100},
]

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
}


@app.get("/stream", response_class=EventSourceResponse)
async def stream(
    last_event_id: Annotated[str | None, Header(alias="Last-Event-ID")] = None,
) -> AsyncIterator[ServerSentEvent]:
    start = int(last_event_id) if last_event_id is not None else 0
    for item in events:
        if int(item["id"]) <= start:
            continue
        await asyncio.sleep(0.01)
        yield ServerSentEvent(
            data=item,
            event="message",
            id=str(item["id"]),
            retry=3000,
        )
    yield ServerSentEvent(comment="stream closed")


@app.get("/stream/raw", response_class=EventSourceResponse)
async def stream_raw() -> AsyncIterator[ServerSentEvent]:
    for index, line in enumerate(["第一行原始文本", "第二行原始文本", "第三行原始文本"], start=1):
        await asyncio.sleep(0.01)
        yield ServerSentEvent(raw_data=line, event="raw", id=str(index))


@app.get("/stream/keepalive", response_class=EventSourceResponse)
async def stream_keepalive() -> AsyncIterator[ServerSentEvent]:
    for tick in range(1, 4):
        await asyncio.sleep(0.01)
        yield ServerSentEvent(comment=f"keep-alive {tick}")
        yield ServerSentEvent(data={"tick": tick}, id=str(tick), retry=5000)


@app.get("/stream/text")
async def stream_text() -> StreamingResponse:
    async def event_source() -> AsyncIterator[str]:
        for item in events:
            await asyncio.sleep(0.01)
            yield f"id: {item['id']}\ndata: {item}\n\n"
        yield ": bye\n\n"

    return StreamingResponse(
        event_source(),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )

if __name__ == "__main__":
    pass
