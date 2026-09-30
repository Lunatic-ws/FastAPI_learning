# 练习68：HTTP基本认证（HTTP Basic Auth）
# 本练习文件只有注释，请在下方编写代码实现

import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

"""
任务1: 基本认证方案
要求:
- 使用 HTTPBasic() 创建basic_scheme
- 创建依赖get_username，接收 credentials: HTTPBasicCredentials = Depends(basic_scheme)
- 返回credentials.username
- 在/docs中观察Basic认证的用户名密码输入界面
"""

basic_scheme = HTTPBasic()

CURRENT_USER = "admin"
CURRENT_PASSWORD = "password123"
BASIC_HEADERS = {"WWW-Authenticate": "Basic"}


def get_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(basic_scheme)],
) -> str:
    return credentials.username

"""
任务2: 安全比较凭据
要求:
- 使用 secrets.compare_digest 分别比较用户名和密码
- 正确凭据设为"admin"/"password123"
- 在注释中回答：为什么不直接用==比较（提示：时序攻击）
"""


def verify_basic_credentials(username: str, password: str) -> bool:
    username_ok = secrets.compare_digest(username, CURRENT_USER)
    password_ok = secrets.compare_digest(password, CURRENT_PASSWORD)
    return username_ok and password_ok


DOC_TASK2 = {
    "为什么不直接用==比较": (
        "字符串==在内容不同时会立刻返回，耗时随匹配前缀长度变化，"
        "攻击者可通过测量响应时间逐字节猜测凭据（时序攻击）。"
        "secrets.compare_digest使用常数时间算法，耗时与内容无关，无法据此推断信息。"
    ),
}

"""
任务3: 401与WWW-Authenticate头
要求:
- 凭据错误时抛出HTTPException(401)
- 设置 headers={"WWW-Authenticate": "Basic"}
- 在注释中回答：这个头的作用是什么
"""


def verify_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(basic_scheme)],
) -> str:
    if not verify_basic_credentials(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="错误的用户名或密码",
            headers=BASIC_HEADERS,
        )
    return credentials.username


DOC_TASK3 = {
    "WWW-Authenticate头的作用": (
        "这是HTTP规范的认证质询（challenge）头。"
        "返回401时带上它，浏览器才知道该弹出Basic登录框并按Base64方式重发凭据，"
        "客户端也能识别这是哪种认证方式（Basic / Bearer / Digest等）并做出相应处理。"
    ),
}

"""
任务4: 受保护接口
要求:
- 创建GET接口 /protected/，依赖get_username返回"欢迎, {username}"
- 用浏览器直接访问测试弹出式登录框的效果
"""


@app.get("/protected/")
def protected(username: Annotated[str, Depends(verify_credentials)]) -> dict[str, str]:
    return {"message": f"欢迎, {username}"}


@app.get("/whoami/")
def whoami(username: Annotated[str, Depends(get_username)]) -> dict[str, str]:
    return {"username": username}


@app.get("/admin/")
def admin_only(username: Annotated[str, Depends(verify_credentials)]) -> dict[str, str]:
    if username != CURRENT_USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限",
            headers=BASIC_HEADERS,
        )
    return {"username": username, "role": "admin"}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)