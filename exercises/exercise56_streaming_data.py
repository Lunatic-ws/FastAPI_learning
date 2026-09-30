# 练习56：流式数据（Streaming Response）
# 本练习文件只有注释，请在下方编写代码实现
import asyncio
import json
import tempfile
from collections.abc import AsyncIterator, Iterator
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse

app = FastAPI()

"""
任务1: 同步生成器流式响应
要求:
- 使用 StreamingResponse 配合同步生成器
- 生成器逐个产出数字0-9，每个数字带换行符
- 创建GET接口 /stream-sync/ 返回流式结果
"""
def iter_numbers() -> Iterator[str]:
    for number in range(10):
        yield f"{number}\n"


@app.get("/stream-sync/")
def stream_sync() -> StreamingResponse:
    return StreamingResponse(iter_numbers(), media_type="text/plain")

"""
任务2: 异步生成器流式响应
要求:
- 使用 async def 生成器，asyncio.sleep(0.5) 模拟耗时产出
- 逐秒产出当前时间字符串，共产出5次
- 创建GET接口 /stream-async/
"""
async def iter_timestamps() -> AsyncIterator[str]:
    for index in range(5):
        await asyncio.sleep(0.5)
        stamp = datetime.now().isoformat(timespec="seconds")
        yield f"{index + 1} {stamp}\n"


@app.get("/stream-async/")
async def stream_async() -> StreamingResponse:
    return StreamingResponse(iter_timestamps(), media_type="text/plain")

"""
任务3: 大文件分块返回
要求:
- 模拟一个1MB的bytes数据
- 实现 iter_file(data, chunk_size=65536) 生成器按块产出
- 创建GET接口 /download/ 用 StreamingResponse 返回，media_type="application/octet-stream"
- 添加 Content-Disposition 响应头模拟文件下载
"""
FILE_DATA = bytes(range(256)) * 4096


def iter_file(data: bytes, chunk_size: int = 65536) -> Iterator[bytes]:
    for start in range(0, len(data), chunk_size):
        yield data[start : start + chunk_size]


@app.get("/download/")
def download() -> StreamingResponse:
    return StreamingResponse(
        iter_file(FILE_DATA),
        media_type="application/octet-stream",
        headers={"Content-Disposition": 'attachment; filename="payload.bin"'},
    )

"""
任务4: 流式JSON
要求:
- 创建GET接口 /stream-json/
- 使用生成器逐行产出 json.dumps 的对象（如 {"value": n}）
- 设置正确的 media_type
"""
def iter_json_values() -> Iterator[str]:
    for value in range(5):
        yield json.dumps({"value": value}, ensure_ascii=False) + "\n"


@app.get("/stream-json/")
def stream_json() -> StreamingResponse:
    return StreamingResponse(iter_json_values(), media_type="application/x-ndjson")


def iter_csv_rows(rows: int = 3) -> Iterator[str]:
    yield "id,name\n"
    for index in range(1, rows + 1):
        yield f"{index},user-{index}\n"


@app.get("/stream-csv/")
def stream_csv() -> StreamingResponse:
    return StreamingResponse(iter_csv_rows(), media_type="text/csv")


TEMP_DOWNLOAD = Path(tempfile.gettempdir()) / "exercise56_streaming_download.txt"
TEMP_DOWNLOAD.write_text(
    "".join(f"line {index}\n" for index in range(1, 1001)),
    encoding="utf-8",
    newline="\n",
)


@app.get("/download-file/")
def download_file() -> FileResponse:
    return FileResponse(
        TEMP_DOWNLOAD,
        media_type="text/plain",
        filename=TEMP_DOWNLOAD.name,
    )

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)