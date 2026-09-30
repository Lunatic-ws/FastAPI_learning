# 练习52：前端（Frontend）
# 要求：根据注释要求实现相应的FastAPI应用
import base64
import tempfile
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

TEMP_ROOT = Path(tempfile.gettempdir()) / "fastapi_ex52_static"
DIST_DIR = TEMP_ROOT / "dist"
TEMP_ROOT.mkdir(parents=True, exist_ok=True)
DIST_DIR.mkdir(parents=True, exist_ok=True)

INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>FastAPI 前端</title>
  <script src="/static/app.js" defer></script>
</head>
<body>
  <h1>FastAPI 前端构建产物</h1>
  <p>app.frontend() 把 dist 构建目录作为低优先级路由挂载到应用上：</p>
  <ul>
    <li>后端 API 路径优先匹配</li>
    <li>未匹配的路径再回退到 dist 中的静态文件</li>
    <li>因此前端与 API 可以由同一个 FastAPI 应用一起提供</li>
  </ul>
  <pre id="output">loading...</pre>
</body>
</html>
"""

APP_JS = """async function main() {
  const response = await fetch("/api/data/");
  const payload = await response.json();
  document.getElementById("output").textContent = JSON.stringify(payload);
}

document.addEventListener("DOMContentLoaded", main);
"""

LOGO_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)

(DIST_DIR / "index.html").write_text(INDEX_HTML, encoding="utf-8")
(DIST_DIR / "app.js").write_text(APP_JS, encoding="utf-8")
(DIST_DIR / "logo.png").write_bytes(LOGO_PNG)
(TEMP_ROOT / "static").mkdir(parents=True, exist_ok=True)
(TEMP_ROOT / "static" / "app.js").write_text(APP_JS, encoding="utf-8")
(TEMP_ROOT / "static" / "logo.png").write_bytes(LOGO_PNG)


# 题目1：认识app.frontend()
# 在注释中回答：app.frontend() 的作用是什么
# 它是如何把前端构建产物与后端API一起提供的
app = FastAPI(title="前端示例", version="1.0.0")
app.frontend("/", directory=DIST_DIR)
app.mount("/static", StaticFiles(directory=TEMP_ROOT / "static"), name="static")


@app.get("/index.html", include_in_schema=False)
def read_index() -> FileResponse:
    return FileResponse(DIST_DIR / "index.html")


# 题目2：为独立前端配置CORS
# 创建FastAPI应用并配置CORSMiddleware
# allow_origins=["http://localhost:5173"]（模拟Vite开发服务器）
# 允许的methods为 ["*"]，allow_headers为 ["*"]
app2 = FastAPI(title="独立前端API", version="1.0.0")
app2.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 题目3：提供API供前端调用
# 创建GET接口 /api/data/ 返回 {"items": ["装修", "设计", "施工"]}
# 创建POST接口 /api/echo/ 接收message(str)并原样返回
class EchoRequest(BaseModel):
    message: str


@app2.get("/api/data/")
def read_data() -> dict[str, list[str]]:
    return {"items": ["装修", "设计", "施工"]}


@app2.post("/api/echo/")
def echo(payload: EchoRequest) -> dict[str, str]:
    return {"message": payload.message}


# 题目4：跨域流程理解（在注释中回答）
# 浏览器在什么情况下会发起CORS预检(OPTIONS)请求
# 如果前端报错CORS policy: No 'Access-Control-Allow-Origin'，应如何排查
@app2.get("/api/cors-info/")
def read_cors_info() -> dict[str, object]:
    return {
        "allow_origins": ["http://localhost:5173"],
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "preflight_trigger": (
            "非简单请求：method不是GET/HEAD/POST，或带有"
            "Content-Type: application/json、Authorization等自定义头"
        ),
        "preflight_request": (
            "OPTIONS 请求，必须同时携带 Origin 与 Access-Control-Request-Method"
        ),
        "debug_steps": [
            "确认请求的Origin与allow_origins完全一致（协议、主机、端口都不能差）",
            "确认后端已添加CORSMiddleware且中间件顺序未被其它中间件覆盖响应头",
            "在浏览器Network面板查看OPTIONS预检是否返回200及Access-Control-Allow-*头",
            "带凭证的请求不能用通配符*，必须写明源、方法与头部",
        ],
    }


# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
