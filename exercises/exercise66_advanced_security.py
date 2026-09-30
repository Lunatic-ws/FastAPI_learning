# 练习66: 高级安全
# 本练习文件只有注释，请在下方编写代码实现

import base64
import hashlib
import hmac
import json
import secrets
from collections.abc import Callable
from typing import Annotated, Any

from fastapi import Depends, FastAPI, Header, HTTPException, Security, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

"""
任务1: HTTP Basic Auth - 基础实现
要求:
- 使用 HTTPBasic 和 HTTPBasicCredentials
- 创建路由 /login/ 要求Basic Auth认证
- 返回当前用户的用户名和密码（实际项目中不应返回密码）
- 使用 secrets.compare_digest 比较用户名和密码
- 验证失败返回401状态码和 WWW-Authenticate header
- 测试用户: username="admin", password="secret123"
"""

basic_scheme = HTTPBasic()
BASIC_HEADERS = {"WWW-Authenticate": "Basic"}


def verify_secret(candidate: str, expected: str) -> bool:
    return secrets.compare_digest(candidate.encode("utf-8"), expected.encode("utf-8"))


@app.get("/login/")
def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(basic_scheme)],
) -> dict[str, Any]:
    valid_user = verify_secret(credentials.username, "admin")
    valid_password = verify_secret(credentials.password, "secret123")
    if not (valid_user and valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="错误的用户名或密码",
            headers=BASIC_HEADERS,
        )
    return {"username": credentials.username, "password": credentials.password}

"""
任务2: HTTP Basic Auth - 用户验证
要求:
- 创建模拟用户数据库 {"admin": "password123", "user1": "pass456"}
- 实现 get_current_user() 依赖
- 依赖验证用户名和密码是否匹配数据库
- 验证失败抛出 HTTPException
- 创建 /profile/ 路由返回当前用户信息
"""

BASIC_USERS_DB: dict[str, str] = {
    "admin": "password123",
    "user1": "pass456",
}


def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(basic_scheme)],
) -> dict[str, str]:
    expected_password = BASIC_USERS_DB.get(credentials.username)
    if expected_password is None or not verify_secret(credentials.password, expected_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="错误的用户名或密码",
            headers=BASIC_HEADERS,
        )
    role = "admin" if credentials.username == "admin" else "user"
    return {"username": credentials.username, "role": role}


@app.get("/profile/")
def read_profile(user: Annotated[dict[str, str], Depends(get_current_user)]) -> dict[str, Any]:
    return {"user": user}

"""
任务3: OAuth2 Scopes - 基础实现
要求:
- 使用 OAuth2PasswordBearer 定义 scopes
- 定义scopes: "read", "write", "admin"
- 实现 create_token() 路由，接收 username 和 scopes 列表，返回JWT token
- token中包含用户信息和scopes
- 实现 get_current_user() 依赖解析token
"""

SECRET_KEY = "3f8a1c9e2b7d4056a1e8f3c9d2b7a6054e1f8c3d9a2b6e4f1c7d0a3b5e9f2c"
ALGORITHM = "HS256"
AVAILABLE_SCOPES = ["read", "write", "admin"]
BEARER_HEADERS = {"WWW-Authenticate": "Bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={scope: scope for scope in AVAILABLE_SCOPES})


class TokenError(Exception):
    pass


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(segment: str) -> bytes:
    return base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4))


def _sign(signing_input: bytes) -> bytes:
    return hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()


def encode_token(payload: dict[str, Any]) -> str:
    header = {"alg": ALGORITHM, "typ": "JWT"}
    segments = [
        _b64url_encode(json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")),
        _b64url_encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")),
    ]
    signing_input = ".".join(segments).encode("ascii")
    segments.append(_b64url_encode(_sign(signing_input)))
    return ".".join(segments)


def decode_token(token: str) -> dict[str, Any]:
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


class ScopedUser(BaseModel):
    username: str
    scopes: list[str] = []


class TokenRequest(BaseModel):
    username: str
    scopes: list[str] = []


@app.post("/create-token/")
def create_token(request: TokenRequest) -> dict[str, Any]:
    granted = [scope for scope in request.scopes if scope in AVAILABLE_SCOPES]
    token = encode_token({"sub": request.username, "scopes": granted})
    return {"access_token": token, "token_type": "bearer", "scopes": granted}


def get_scoped_user(token: Annotated[str, Depends(oauth2_scheme)]) -> ScopedUser:
    try:
        payload = decode_token(token)
    except TokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的凭据",
            headers=BEARER_HEADERS,
        ) from exc
    username = payload.get("sub")
    if not isinstance(username, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的凭据",
            headers=BEARER_HEADERS,
        )
    raw_scopes = payload.get("scopes") or []
    return ScopedUser(username=username, scopes=[str(scope) for scope in raw_scopes])


@app.get("/scoped-user/")
def read_scoped_user(user: Annotated[ScopedUser, Depends(get_scoped_user)]) -> dict[str, Any]:
    return {"username": user.username, "scopes": user.scopes}

"""
任务4: OAuth2 Scopes - 权限验证
要求:
- 实现 require_scopes() 依赖工厂，接收 required_scopes 列表
- 验证用户token中是否包含所有required_scopes
- 权限不足时返回403 Forbidden
- 创建路由:
  - /read-data/ 要求 "read" scope
  - /write-data/ 要求 "write" scope
  - /admin-panel/ 要求 "admin" scope
"""


def require_scopes(required_scopes: list[str]) -> Callable[..., ScopedUser]:
    def dependency(user: Annotated[ScopedUser, Depends(get_scoped_user)]) -> ScopedUser:
        missing = [scope for scope in required_scopes if scope not in user.scopes]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"缺少必要的权限: {', '.join(missing)}",
            )
        return user

    dependency.__name__ = "require_" + "_".join(
        scope.replace(":", "_") for scope in required_scopes
    )
    return dependency


require_read = require_scopes(["read"])
require_write = require_scopes(["write"])
require_admin_scope = require_scopes(["admin"])


@app.get("/read-data/")
def read_data(user: Annotated[ScopedUser, Security(require_read)]) -> dict[str, Any]:
    return {"user": user.username, "data": ["公开数据"]}


@app.get("/write-data/")
def write_data(user: Annotated[ScopedUser, Security(require_write)]) -> dict[str, Any]:
    return {"user": user.username, "written": True}


@app.get("/admin-panel/")
def admin_panel(user: Annotated[ScopedUser, Security(require_admin_scope)]) -> dict[str, Any]:
    return {"user": user.username, "panel": "admin"}

"""
任务5: OAuth2 Scopes - 完整流程
要求:
- 实现完整的OAuth2流程:
  1. POST /token/ - 用户登录，返回access_token（含scopes）
  2. GET /users/me/ - 返回当前用户信息（要求认证）
  3. GET /items/ - 返回项目列表（要求 "items:read" scope）
  4. POST /items/ - 创建项目（要求 "items:write" scope）
- 使用JWT token，包含 sub（用户ID）和 scopes
- 实现权限验证中间件
"""

SCOPED_USERS_DB: dict[str, dict[str, Any]] = {
    "alice": {"username": "alice", "full_name": "Alice Wang", "disabled": False},
    "bob": {"username": "bob", "full_name": "Bob Li", "disabled": True},
}

items_store: dict[int, dict[str, Any]] = {
    1: {"id": 1, "name": "Hammer"},
    2: {"id": 2, "name": "Nail"},
}


class LoginRequest(BaseModel):
    username: str
    scopes: list[str] = []


class ItemIn(BaseModel):
    name: str


def get_flow_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, Any]:
    try:
        payload = decode_token(token)
    except TokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的凭据",
            headers=BEARER_HEADERS,
        ) from exc
    username = payload.get("sub")
    user = SCOPED_USERS_DB.get(username) if isinstance(username, str) else None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的凭据",
            headers=BEARER_HEADERS,
        )
    raw_scopes = payload.get("scopes") or []
    return {**user, "scopes": [str(scope) for scope in raw_scopes]}


def require_flow_scopes(required_scopes: list[str]) -> Callable[..., dict[str, Any]]:
    def dependency(user: Annotated[dict[str, Any], Depends(get_flow_user)]) -> dict[str, Any]:
        if user["disabled"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        missing = [scope for scope in required_scopes if scope not in user["scopes"]]
        if missing:
            authenticate_value = (
                f'Bearer scope="{required_scopes[0]}"'
                if len(required_scopes) == 1
                else f'Bearer scope="{required_scopes[0]} {required_scopes[1]}"'
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
        return user

    dependency.__name__ = "require_" + "_".join(
        scope.replace(":", "_") for scope in required_scopes
    )
    return dependency


require_authenticated = require_flow_scopes([])
require_items_read = require_flow_scopes(["items:read"])
require_items_write = require_flow_scopes(["items:write"])


@app.post("/token/")
def login_for_token(request: LoginRequest) -> dict[str, Any]:
    user = SCOPED_USERS_DB.get(request.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="错误的用户名或密码",
            headers=BEARER_HEADERS,
        )
    if user["disabled"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该用户已被禁用")
    granted = [scope for scope in request.scopes if scope in ("items:read", "items:write")]
    token = encode_token({"sub": request.username, "scopes": granted})
    return {"access_token": token, "token_type": "bearer", "scopes": granted}


@app.get("/users/me/")
def read_flow_user(
    user: Annotated[dict[str, Any], Depends(require_authenticated)],
) -> dict[str, Any]:
    return {key: value for key, value in user.items() if key != "disabled"}


@app.get("/items/")
def list_flow_items(
    user: Annotated[dict[str, Any], Security(require_items_read)],
) -> list[dict[str, Any]]:
    return list(items_store.values())


@app.post("/items/")
def create_flow_item(
    item: ItemIn,
    user: Annotated[dict[str, Any], Security(require_items_write)],
) -> dict[str, Any]:
    new_id = max(items_store, default=0) + 1
    record = {"id": new_id, "name": item.name, "owner": user["username"]}
    items_store[new_id] = record
    return record

"""
任务6: 组合认证 - 多种认证方式
要求:
- 实现支持两种认证方式:
  1. API Key (通过header X-API-Key)
  2. Bearer Token (OAuth2)
- 创建 get_current_user() 依赖，自动检测使用哪种认证
- API Key列表: ["key1", "key2", "key3"]
- 模拟用户数据库，包含用户信息和token
- 路由 /protected/ 支持任意一种认证方式
"""

API_KEYS = ["key1", "key2", "key3"]
COMBINED_USERS_DB: dict[str, dict[str, Any]] = {
    "alice": {"username": "alice", "role": "admin"},
    "bob": {"username": "bob", "role": "user"},
}
COMBINED_TOKENS: dict[str, str] = {
    "token-alice": "alice",
    "token-bob": "bob",
}


def get_combined_user(
    api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
    authorization: Annotated[str | None, Header()] = None,
) -> dict[str, Any]:
    if api_key is not None:
        valid = any(secrets.compare_digest(api_key, known) for known in API_KEYS)
        if not valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的API Key",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        return {"username": "api-key-user", "role": "service", "auth": "api_key"}
    if authorization is not None:
        scheme, _, credentials = authorization.partition(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="不支持的认证方式",
                headers=BEARER_HEADERS,
            )
        username = COMBINED_TOKENS.get(credentials)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的凭据",
                headers=BEARER_HEADERS,
            )
        return {**COMBINED_USERS_DB[username], "auth": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="缺少凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/protected/")
def read_protected(user: Annotated[dict[str, Any], Depends(get_combined_user)]) -> dict[str, Any]:
    return user

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)