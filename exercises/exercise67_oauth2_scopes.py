# 练习67：OAuth2作用域（OAuth2 Scopes）
# 本练习文件只有注释，请在下方编写代码实现

import base64
import hashlib
import hmac
import json
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes

app = FastAPI()

"""
任务1: 声明作用域
要求:
- 创建OAuth2PasswordBearer，scopes参数声明：
  items: read / items: write / users: read
- 在/docs的Authorize面板中观察scopes勾选框
"""

SCOPES = {
    "items:read": "读取项目",
    "items:write": "写入项目",
    "users:read": "读取用户",
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes=SCOPES,
    auto_error=True,
)

"""
任务2: 创建带scopes的token
要求:
- POST /token/ 接收OAuth2PasswordRequestForm，form.scopes即选中的作用域列表
- 将scopes写入JWT的"scopes"声明中
"""

SECRET_KEY = "c3a9e1b74d8f4026b5e7c1a9d3f6082b4e6d8c0a2f5b7d9e1c3a5f7b9d1e3c5a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
BEARER_HEADERS = {"WWW-Authenticate": "Bearer"}

fake_users_db: dict[str, dict[str, Any]] = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Wang",
        "email": "alice@example.com",
        "disabled": False,
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Li",
        "email": "bob@example.com",
        "disabled": False,
    },
    "carol": {
        "username": "carol",
        "full_name": "Carol Zhao",
        "email": "carol@example.com",
        "disabled": True,
    },
}


class TokenError(Exception):
    pass


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(segment: str) -> bytes:
    return base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4))


def _sign(signing_input: bytes) -> bytes:
    return hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()


def jwt_encode(payload: dict[str, Any]) -> str:
    header = {"alg": ALGORITHM, "typ": "JWT"}
    segments = [
        _b64url_encode(json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")),
        _b64url_encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")),
    ]
    signing_input = ".".join(segments).encode("ascii")
    segments.append(_b64url_encode(_sign(signing_input)))
    return ".".join(segments)


def jwt_decode(token: str) -> dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise TokenError("token格式不正确")
    header_segment, payload_segment, signature_segment = parts
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    try:
        signature = _b64url_decode(signature_segment)
        header = json.loads(_b64url_decode(header_segment))
        payload = json.loads(_b64url_decode(payload_segment))
    except (TypeError, ValueError) as exc:
        raise TokenError("token内容无法解析") from exc
    if not hmac.compare_digest(signature, _sign(signing_input)):
        raise TokenError("签名校验失败")
    if not isinstance(payload, dict) or header.get("alg") != ALGORITHM:
        raise TokenError("不支持的签名算法或载荷格式")
    return payload


@app.post("/token/")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict[str, Any]:
    user = fake_users_db.get(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="错误的用户名或密码",
            headers=BEARER_HEADERS,
        )
    if user["disabled"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    granted = [scope for scope in form_data.scopes if scope in SCOPES]
    token = jwt_encode({"sub": user["username"], "scopes": granted})
    return {"access_token": token, "token_type": "bearer", "scopes": granted}

"""
任务3: 校验作用域
要求:
- get_current_user依赖中接收 security_scopes: SecurityScopes 参数
- 解码JWT后逐层检查token中的scopes是否覆盖security_scopes.scopes
- 使用 Security(get_current_user, scopes=["items:read"]) 声明接口依赖
"""


def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dict[str, Any]:
    try:
        payload = jwt_decode(token)
    except TokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的凭据",
            headers=BEARER_HEADERS,
        ) from exc
    username = payload.get("sub")
    user = fake_users_db.get(username) if isinstance(username, str) else None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的凭据",
            headers=BEARER_HEADERS,
        )
    if user["disabled"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    token_scopes = [str(scope) for scope in (payload.get("scopes") or [])]
    missing = [scope for scope in security_scopes.scopes if scope not in token_scopes]
    if missing:
        authenticate_value = (
            f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
    return {**user, "scopes": token_scopes}


items_store: dict[int, dict[str, Any]] = {
    1: {"id": 1, "name": "Hammer"},
    2: {"id": 2, "name": "Nail"},
}

"""
任务4: 权限不足返回403
要求:
- scopes不满足时抛出HTTPException(403)，detail中带上缺失的scopes
- 创建3个接口验证：/items/（读）、/items-write/（写）、/users/（用户读）
- 分别以不同scopes组合的token测试
"""


@app.get("/items/")
def read_items(
    user: Annotated[dict[str, Any], Security(get_current_user, scopes=["items:read"])],
) -> list[dict[str, Any]]:
    return list(items_store.values())


@app.post("/items-write/")
def write_items(
    user: Annotated[dict[str, Any], Security(get_current_user, scopes=["items:write"])],
) -> dict[str, Any]:
    new_id = max(items_store, default=0) + 1
    record = {"id": new_id, "name": "Screw", "owner": user["username"]}
    items_store[new_id] = record
    return record


@app.get("/users/")
def read_users(
    user: Annotated[dict[str, Any], Security(get_current_user, scopes=["users:read"])],
) -> list[dict[str, Any]]:
    return [
        {"username": entry["username"], "full_name": entry["full_name"]}
        for entry in fake_users_db.values()
        if not entry["disabled"]
    ]


@app.get("/users/me/")
def read_users_me(
    user: Annotated[dict[str, Any], Security(get_current_user, scopes=["users:read"])],
) -> dict[str, Any]:
    return {key: value for key, value in user.items() if key != "disabled"}


@app.get("/items-open/")
def read_items_open(
    user: Annotated[dict[str, Any], Security(get_current_user)],
) -> list[dict[str, Any]]:
    return list(items_store.values())


@app.get("/items-admin-only/")
def read_items_admin_only(
    user: Annotated[dict[str, Any], Security(get_current_user)],
) -> dict[str, Any]:
    missing = [scope for scope in ("items:read", "users:read") if scope not in user["scopes"]]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"缺少必要的权限: {', '.join(missing)}",
        )
    return {"user": user["username"], "items": list(items_store.values())}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)