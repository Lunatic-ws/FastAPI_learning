# 练习60：自定义Response类（Custom Response Class）
# 本练习文件只有注释，请在下方编写代码实现
import json
from datetime import datetime
from decimal import Decimal
from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response


class CompactJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content, ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")


class IndentedJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(content, ensure_ascii=False, indent=2).encode("utf-8")


app = FastAPI(default_response_class=CompactJSONResponse)

"""
任务1: 使用ORJSONResponse
要求:
- pip install orjson 后，创建应用设置 default_response_class=ORJSONResponse
- （未安装时在注释中记录该配置方式即可）
- 创建一个返回大量嵌套数据的接口，对比orjson的转义/性能特点（注释回答）
"""
@app.get("/orjson/")
def get_orjson_style() -> dict:
    return {
        "library": "FastAPI 教程",
        "records": [
            {
                "id": record_id,
                "name": f"条目{record_id}",
                "tags": ["中文标签", "json", "序列化"],
                "meta": {"active": True, "score": record_id * 1.5, "note": None},
            }
            for record_id in range(1, 21)
        ],
    }


"""
任务2: 使用UJSONResponse
要求:
- 创建GET接口 /ujson/
- 使用 response_class=UJSONResponse
- （注释说明：需要 pip install ujson，ujson不那么严格，是"最优努力"模式）
"""
class UJSONStyleResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=True,
            separators=(", ", ": "),
            default=str,
        ).encode("utf-8")


@app.get("/ujson/", response_class=UJSONStyleResponse)
def get_ujson_style() -> dict:
    return {
        "message": "最优努力模式",
        "amount": Decimal("3.14"),
        "created_at": datetime(2026, 1, 1, 12, 0, 0),
    }


"""
任务3: 自定义XMLResponse
要求:
- 创建XMLResponse类继承Response，media_type="application/xml"
- 创建GET接口 /xml/ 返回简单的XML内容
"""
class XMLResponse(Response):
    media_type = "application/xml"

    def render(self, content: Any) -> bytes:
        rows = content if isinstance(content, list) else [content]
        lines = ['<?xml version="1.0" encoding="utf-8"?>']
        for row in rows:
            lines.extend(f"  <{key}>{value}</{key}>" for key, value in row.items())
        return ("\n".join(lines) + "\n").encode("utf-8")


@app.get("/xml/", response_class=XMLResponse)
def get_xml() -> dict:
    return {"name": "Portal Gun", "price": 42.0}


"""
任务4: 覆盖优先级
要求:
- 应用级设置default_response_class
- 单个路由显式设置response_class
- 在注释中回答：路由级和应用级配置哪个生效
"""
@app.get("/default-class/")
def get_default_class() -> dict:
    return {"level": "app", "class": "CompactJSONResponse", "message": "应用级默认生效"}


@app.get("/explicit-class/", response_class=IndentedJSONResponse)
def get_explicit_class() -> dict:
    return {"level": "route", "class": "IndentedJSONResponse", "message": "路由级覆盖应用级"}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
