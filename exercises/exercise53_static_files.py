# 练习53：静态文件
# 要求：配置FastAPI应用提供静态文件服务
import base64
import os
import tempfile
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_ROOT = Path(tempfile.gettempdir()) / "fastapi_ex53_static"

LOGO_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)

STYLE_CSS = "body { font-family: sans-serif; } .title { color: #009485; }"

SCRIPT_JS = "document.addEventListener('DOMContentLoaded', () => console.log('static ok'));"


def build_static_dir(name: str, index_title: str) -> Path:
    directory = STATIC_ROOT / name
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "index.html").write_text(
        f"<!DOCTYPE html><html><head><title>{index_title}</title>"
        f'<link rel="stylesheet" href="/static/style.css"></head>'
        f"<body><h1>{index_title}</h1>"
        f'<script src="/static/script.js"></script></body></html>',
        encoding="utf-8",
    )
    (directory / "style.css").write_text(STYLE_CSS, encoding="utf-8")
    (directory / "script.js").write_text(SCRIPT_JS, encoding="utf-8")
    (directory / "logo.png").write_bytes(LOGO_PNG)
    return directory


STATIC_DIR = build_static_dir("static", "公共静态资源")
UPLOADS_DIR = build_static_dir("uploads", "用户上传文件")
ASSETS_DIR = build_static_dir("assets", "前端资源")
STATIC_V1_DIR = build_static_dir("static_v1", "v1 静态资源")
STATIC_V2_DIR = build_static_dir("static_v2", "v2 静态资源")

app = FastAPI(title="静态文件服务", version="1.0.0")


# 题目1：基本静态文件配置
# 创建一个FastAPI应用，挂载"static"目录到"/static"路径
# 目录结构提示：
# static/
#   - style.css
#   - script.js
#   - logo.png
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")


# 题目2：多静态目录配置
# 配置三个静态文件目录：
# - "/static" -> directory="static" (公共静态资源)
# - "/uploads" -> directory="uploads" (用户上传文件)
# - "/assets" -> directory="assets" (前端资源)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR, html=True), name="uploads")
app.mount("/assets", StaticFiles(directory=ASSETS_DIR, html=True), name="assets")


# 题目3：版本化静态资源
# 为API的不同版本提供不同的静态文件目录：
# - "/v1/static" -> directory="static_v1"
# - "/v2/static" -> directory="static_v2"
app.mount(
    "/v1/static", StaticFiles(directory=STATIC_V1_DIR, html=True), name="v1_static"
)
app.mount(
    "/v2/static", StaticFiles(directory=STATIC_V2_DIR, html=True), name="v2_static"
)


@app.get("/files/logo.png", include_in_schema=False)
def read_logo() -> FileResponse:
    return FileResponse(STATIC_DIR / "logo.png", media_type="image/png")


@app.get("/files/{name}")
def read_static_file(name: str) -> FileResponse:
    return FileResponse(STATIC_DIR / name)


# 题目4：条件挂载
# 根据环境变量决定是否挂载静态文件
# - 环境变量ENV为"development"时挂载
# - 其他环境不挂载
ENV = os.getenv("ENV", "development")

app2 = FastAPI(title="条件挂载静态文件", version="1.0.0")

if ENV == "development":
    app2.mount(
        "/static", StaticFiles(directory=STATIC_DIR, html=True), name="static"
    )


@app2.get("/config")
def read_config() -> dict[str, object]:
    mounted = any(
        getattr(route, "path", None) == "/static" for route in app2.router.routes
    )
    return {"env": ENV, "static_mounted": mounted}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
