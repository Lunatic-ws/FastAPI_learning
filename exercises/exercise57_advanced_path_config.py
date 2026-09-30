# 练习57：路径操作高级配置（Response Class）
# 本练习文件只有注释，请在下方编写代码实现
import importlib.util
import json
from typing import Annotated, Any

from fastapi import Depends, FastAPI, Header, HTTPException, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()

"""
任务1: 返回纯文本
要求:
- 创建GET接口 /plain/
- 使用 response_class=PlainTextResponse 返回纯文本"Hello Plain"
- 对比不设置response_class时返回JSON的差异
"""
@app.get("/plain/", response_class=PlainTextResponse)
def plain() -> str:
    return "Hello Plain"


@app.get("/json-default/")
def json_default() -> dict[str, str]:
    return {"message": "Hello JSON"}

"""
任务2: 返回HTML
要求:
- 创建GET接口 /html/
- 使用 response_class=HTMLResponse 直接返回一段HTML字符串（如<h1>标题</h1>）
- 用浏览器或curl -i 观察Content-Type变化
"""
@app.get("/html/", response_class=HTMLResponse)
def html() -> str:
    return "<h1>标题</h1>"

"""
任务3: 应用级默认响应类
要求:
- 创建FastAPI应用时设置 default_response_class=ORJSONResponse
- （注释说明：ORJSONResponse需要 pip install orjson，未安装时可改用UJSONResponse）
- 创建两个接口：一个使用应用默认，一个显式覆盖为PlainTextResponse
"""
class UJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


def default_response_class() -> type[Response]:
    if importlib.util.find_spec("orjson") is not None:
        from fastapi.responses import ORJSONResponse

        return ORJSONResponse
    return UJSONResponse


app3 = FastAPI(default_response_class=default_response_class())


@app3.get("/default/")
def use_app_default() -> dict[str, str]:
    return {"message": "app default response class"}


@app3.get("/default-plain/", response_class=PlainTextResponse)
def override_app_default() -> str:
    return "Hello Plain"

"""
任务4: media_type观察
要求:
- 创建3个接口分别返回JSON/纯文本/HTML
- 用curl -i 查看各自响应头中的content-type并记录在注释中
"""
@app.get("/content-json/")
def content_json() -> dict[str, str]:
    return {"kind": "json"}


@app.get("/content-text/")
def content_text() -> PlainTextResponse:
    return PlainTextResponse("Hello Plain")


@app.get("/content-html/")
def content_html() -> HTMLResponse:
    return HTMLResponse("<h1>标题</h1>")


CONTENT_TYPES = {
    "/plain/": "text/plain; charset=utf-8",
    "/json-default/": "application/json",
    "/html/": "text/html; charset=utf-8",
    "/default/": "application/json",
    "/default-plain/": "text/plain; charset=utf-8",
    "/content-json/": "application/json",
    "/content-text/": "text/plain; charset=utf-8",
    "/content-html/": "text/html; charset=utf-8",
}


@app.get("/files/{file_path:path}")
def read_file_path(file_path: str) -> dict[str, str]:
    return {"file_path": file_path}


@app.get("/numbers/{number:int}")
def read_number(number: int) -> dict[str, int]:
    return {"number": number}


@app.get("/numbers/{number:float}")
def read_float(number: float) -> dict[str, float]:
    return {"number": number}


HexId = Annotated[str, Path(pattern="^[0-9a-f]{8}$")]
Year = Annotated[int, Path(ge=1900, le=2100, description="四位年份")]


@app.get("/hex/{hex_id}")
def read_hex_id(hex_id: HexId) -> dict[str, str]:
    return {"hex_id": hex_id}


@app.get("/stats/{year}")
def read_stats(year: Year) -> dict[str, int]:
    return {"year": year}


class Filters(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    keyword: str | None = Field(default=None, alias="kw", alias_priority=2)
    page: int = Field(default=1, ge=1, alias="p")


@app.get("/search/")
def search(filters: Annotated[Filters, Query()]) -> dict[str, Any]:
    return {"kw": filters.keyword, "page": filters.page}


@app.get("/alias/")
def alias_demo(
    q: Annotated[str | None, Query(alias="query", alias_priority=2)] = None,
    hidden: Annotated[str | None, Query(alias="h")] = None,
) -> dict[str, str | None]:
    return {"q": q, "hidden": hidden}


def verify_internal(x_token: Annotated[str | None, Header()] = None) -> str:
    if x_token != "internal-token":
        raise HTTPException(status_code=401, detail="Invalid internal token")
    return x_token


@app.get("/internal/", include_in_schema=False)
def internal() -> dict[str, str]:
    return {"message": "hidden from openapi"}


@app.get("/hidden-dep/", dependencies=[Depends(verify_internal)], include_in_schema=False)
def hidden_dep() -> dict[str, str]:
    return {"message": "hidden dependency"}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)