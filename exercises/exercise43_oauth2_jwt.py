# 练习43：带JWT的OAuth2（OAuth2 with Password and JWT）
# 要求：根据注释要求实现相应的FastAPI应用
# 说明：需要 pip install pyjwt "passlib[bcrypt]"
import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

app = FastAPI()

AUTH_HEADERS = {"WWW-Authenticate": "Bearer"}

# 题目1：密码哈希
# 创建 pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 实现 verify_password(plain, hashed) 和 get_password_hash(password)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 题目2：模拟用户数据库
# 创建fake_users_db，用户字段包含 hashed_password（用get_password_hash生成）
# 其他字段: username, full_name, email, disabled(bool)

fake_users_db: dict[str, dict[str, Any]] = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Wang",
        "email": "alice@example.com",
        "disabled": False,
        "hashed_password": get_password_hash("secret"),
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Li",
        "email": "bob@example.com",
        "disabled": True,
        "hashed_password": get_password_hash("secret"),
    },
}

# 题目3：JWT的创建与配置
# 定义 SECRET_KEY、ALGORITHM="HS256"、ACCESS_TOKEN_EXPIRE_MINUTES=30
# 实现 create_access_token(data: dict)：
# 在data中拷贝加入 "exp"（过期时间，使用datetime.now(timezone.utc) + timedelta）
# 使用 jwt.encode 生成token

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenError(Exception):
    pass


class InvalidTokenError(TokenError):
    pass


class ExpiredSignatureError(TokenError):
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
        raise InvalidTokenError("token格式不正确")
    header_segment, payload_segment, signature_segment = parts
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    try:
        signature = _b64url_decode(signature_segment)
    except (TypeError, ValueError) as exc:
        raise InvalidTokenError("签名无法解码") from exc
    if not hmac.compare_digest(signature, _sign(signing_input)):
        raise InvalidTokenError("签名校验失败")
    try:
        header = json.loads(_b64url_decode(header_segment))
        payload = json.loads(_b64url_decode(payload_segment))
    except (TypeError, ValueError) as exc:
        raise InvalidTokenError("token内容无法解析") from exc
    if not isinstance(payload, dict) or header.get("alg") != ALGORITHM:
        raise InvalidTokenError("不支持的签名算法或载荷格式")
    expire_at = payload.get("exp")
    if expire_at is not None:
        try:
            expire_timestamp = float(expire_at)
        except (TypeError, ValueError) as exc:
            raise InvalidTokenError("exp字段无效") from exc
        if datetime.now(timezone.utc).timestamp() >= expire_timestamp:
            raise ExpiredSignatureError("token已过期")
    return payload


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = dict(data)
    lifetime = (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    expire = datetime.now(timezone.utc) + lifetime
    to_encode["exp"] = int(expire.timestamp())
    return jwt_encode(to_encode)

# 题目4：登录端点
# 创建POST接口 /token/，校验用户存在、密码verify通过、用户未disabled
# 失败时抛出 HTTPException(401, detail="错误的用户名或密码")
# 成功时返回 create_access_token 生成的JWT

@app.post("/token/")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict:
    user = fake_users_db.get(form_data.username)
    if user is None or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="错误的用户名或密码",
            headers=AUTH_HEADERS,
        )
    if user["disabled"]:
        raise HTTPException(status_code=400, detail="该用户已被禁用")
    return {
        "access_token": create_access_token({"sub": user["username"]}),
        "token_type": "bearer",
    }

# 题目5：解码JWT获取当前用户
# 实现 get_current_user 依赖：jwt.decode 解码token
# 处理 jwt.ExpiredSignatureError（返回401"token已过期"）
# 处理解码失败和用户不存在（返回401"无效的凭据"）
# 实现 get_current_active_user：disabled用户返回400
# 创建 /users/me/ 受保护接口，用 /docs 的Authorize完整测试

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="无效的凭据",
        headers=AUTH_HEADERS,
    )
    try:
        payload = jwt_decode(token)
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=401,
            detail="token已过期",
            headers=AUTH_HEADERS,
        ) from exc
    except TokenError as exc:
        raise credentials_exception from exc
    username = payload.get("sub")
    if not isinstance(username, str) or username not in fake_users_db:
        raise credentials_exception
    return fake_users_db[username]


def get_current_active_user(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/users/me/")
def read_users_me(
    current_user: dict[str, Any] = Depends(get_current_active_user),
) -> dict:
    return {key: value for key, value in current_user.items() if key != "hashed_password"}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
