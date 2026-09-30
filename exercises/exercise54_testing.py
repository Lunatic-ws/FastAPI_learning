# 练习54：测试
# 要求：使用TestClient为FastAPI应用编写测试
from typing import Annotated
from unittest.mock import patch

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

# 题目1：基础测试
# 创建以下应用并编写测试：
# - GET /：返回{"message": "Welcome"}
# - GET /health：返回{"status": "ok"}
# 测试两个路径的status_code和json内容
@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome"}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}


def test_root_status_code_and_json():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome"}


def test_health_status_code_and_json():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_unknown_path_returns_404():
    client = TestClient(app)
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

# 题目2：测试路径参数
# 创建以下应用并编写测试：
# - GET /items/{item_id}：返回{"item_id": item_id}
# 测试：
# - item_id为1时返回正确结果
# - item_id为"abc"时返回正确结果
app2 = FastAPI()


@app2.get("/items/{item_id}")
def read_item(item_id: str) -> dict[str, str]:
    return {"item_id": item_id}


def test_path_parameter_numeric_value():
    client = TestClient(app2)
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": "1"}


def test_path_parameter_string_value():
    client = TestClient(app2)
    response = client.get("/items/abc")
    assert response.status_code == 200
    assert response.json() == {"item_id": "abc"}


def test_path_parameter_missing_segment_returns_404():
    client = TestClient(app2)
    response = client.get("/items")
    assert response.status_code == 404


def test_path_parameter_with_slash_is_not_matched():
    client = TestClient(app2)
    response = client.get("/items/1/extra")
    assert response.status_code == 404

# 题目3：测试查询参数
# 创建以下应用并编写测试：
# - GET /users/：接受skip和limit参数，返回{"skip": skip, "limit": limit}
# 测试：
# - 默认参数值
# - 自定义参数值
app3 = FastAPI()


@app3.get("/users/")
def read_users(skip: int = 0, limit: int = 10) -> dict[str, int]:
    return {"skip": skip, "limit": limit}


def test_query_parameters_defaults():
    client = TestClient(app3)
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {"skip": 0, "limit": 10}


def test_query_parameters_custom_values():
    client = TestClient(app3)
    response = client.get("/users/", params={"skip": 5, "limit": 100})
    assert response.status_code == 200
    assert response.json() == {"skip": 5, "limit": 100}


def test_query_parameters_partial_override():
    client = TestClient(app3)
    response = client.get("/users/", params={"limit": 3})
    assert response.status_code == 200
    assert response.json() == {"skip": 0, "limit": 3}


def test_query_parameters_invalid_value_returns_422():
    client = TestClient(app3)
    response = client.get("/users/", params={"skip": "abc"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "skip"]

# 题目4：测试请求体
# 创建以下应用并编写测试：
# - POST /items/：接受Item模型（name: str, price: float）
# 测试：
# - 正常创建
# - 缺少必填字段返回422错误
app4 = FastAPI()


class Item(BaseModel):
    name: str
    price: float


@app4.post("/items/")
def create_item(item: Item) -> Item:
    return item


def test_body_valid_payload():
    client = TestClient(app4)
    response = client.post("/items/", json={"name": "Hammer", "price": 42.5})
    assert response.status_code == 200
    assert response.json() == {"name": "Hammer", "price": 42.5}


def test_body_missing_required_field_returns_422():
    client = TestClient(app4)
    response = client.post("/items/", json={"name": "Hammer"})
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert errors[0]["loc"] == ["body", "price"]
    assert errors[0]["type"] == "missing"


def test_body_empty_payload_returns_422():
    client = TestClient(app4)
    response = client.post("/items/", json={})
    assert response.status_code == 422
    assert {tuple(error["loc"]) for error in response.json()["detail"]} == {
        ("body", "name"),
        ("body", "price"),
    }


def test_body_wrong_type_returns_422():
    client = TestClient(app4)
    response = client.post("/items/", json={"name": "Hammer", "price": "not-a-number"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "float_parsing"


def test_body_string_number_is_coerced():
    client = TestClient(app4)
    response = client.post("/items/", json={"name": "Hammer", "price": "42.5"})
    assert response.status_code == 200
    assert response.json() == {"name": "Hammer", "price": 42.5}

# 题目5：测试Headers和错误
# 创建以下应用并编写测试：
# - GET /protected/：需要X-API-Key header
# - key正确返回{"status": "authorized"}
# - key错误返回401错误
# 测试：
# - 正确header
# - 错误header
# - 缺少header
app5 = FastAPI()

VALID_API_KEYS = {"secret-key": "admin"}


def verify_api_key(x_api_key: Annotated[str | None, Header()] = None) -> str:
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    role = VALID_API_KEYS.get(x_api_key)
    if role is None:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return role


@app5.get("/protected/")
def read_protected(role: Annotated[str, Depends(verify_api_key)]) -> dict[str, str]:
    return {"status": "authorized"}


def test_protected_with_valid_header():
    client = TestClient(app5)
    response = client.get("/protected/", headers={"X-API-Key": "secret-key"})
    assert response.status_code == 200
    assert response.json() == {"status": "authorized"}


def test_protected_with_invalid_header_returns_401():
    client = TestClient(app5)
    response = client.get("/protected/", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API key"}
    assert response.headers["content-type"].startswith("application/json")


def test_protected_without_header_returns_401():
    client = TestClient(app5)
    response = client.get("/protected/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Missing X-API-Key header"}


def test_protected_with_dependency_overrides():
    app5.dependency_overrides[verify_api_key] = lambda: "admin"
    try:
        client = TestClient(app5)
        response = client.get("/protected/")
        assert response.status_code == 200
        assert response.json() == {"status": "authorized"}
    finally:
        app5.dependency_overrides.clear()


def test_protected_after_overrides_are_cleared_returns_401():
    client = TestClient(app5)
    response = client.get("/protected/")
    assert response.status_code == 401


def test_protected_with_mocked_key_store():
    fake_keys = {"mocked-key": "tester"}
    with patch.dict(VALID_API_KEYS, fake_keys, clear=True):
        client = TestClient(app5)
        assert client.get("/protected/", headers={"X-API-Key": "mocked-key"}).status_code == 200
        assert client.get("/protected/", headers={"X-API-Key": "secret-key"}).status_code == 401
    client = TestClient(app5)
    assert client.get("/protected/", headers={"X-API-Key": "mocked-key"}).status_code == 401


def test_protected_with_test_double_dependency():
    calls: list[str] = []

    def fake_verify_api_key() -> str:
        calls.append("fake_verify_api_key")
        return "admin"

    app5.dependency_overrides[verify_api_key] = fake_verify_api_key
    try:
        client = TestClient(app5)
        response = client.get("/protected/")
        assert response.status_code == 200
        assert response.json() == {"status": "authorized"}
        assert calls == ["fake_verify_api_key"]
    finally:
        app5.dependency_overrides.clear()

# 题目6：测试表单数据
# 创建以下应用并编写测试：
# - POST /login/：接受username和password表单数据
# - 返回{"username": username, "logged_in": True}
# 测试表单提交
app6 = FastAPI()


@app6.post("/login/")
def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> dict[str, object]:
    return {"username": username, "logged_in": True}


def test_login_with_form_data():
    client = TestClient(app6)
    response = client.post(
        "/login/", data={"username": "alice", "password": "secret"}
    )
    assert response.status_code == 200
    assert response.json() == {"username": "alice", "logged_in": True}


def test_login_with_wrong_credentials_still_returns_200():
    client = TestClient(app6)
    response = client.post(
        "/login/", data={"username": "alice", "password": "wrong"}
    )
    assert response.status_code == 200
    assert response.json()["logged_in"] is True


def test_login_missing_field_returns_422():
    client = TestClient(app6)
    response = client.post("/login/", data={"username": "alice"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "password"]


def test_login_with_json_body_returns_422():
    client = TestClient(app6)
    response = client.post(
        "/login/", json={"username": "alice", "password": "secret"}
    )
    assert response.status_code == 422

# 题目7：测试文件上传
# 创建以下应用并编写测试：
# - POST /upload/：接受文件上传
# - 返回{"filename": filename, "size": size}
# 测试文件上传
app7 = FastAPI()


@app7.post("/upload/")
async def upload_file(file: Annotated[UploadFile, File()]) -> dict[str, object]:
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}


def test_upload_text_file():
    client = TestClient(app7)
    response = client.post(
        "/upload/",
        files={"file": ("test.txt", b"hello world", "text/plain")},
    )
    assert response.status_code == 200
    assert response.json() == {"filename": "test.txt", "size": 11}


def test_upload_binary_file():
    client = TestClient(app7)
    payload = bytes(range(256)) * 8
    response = client.post(
        "/upload/", files={"file": ("blob.bin", payload, "application/octet-stream")}
    )
    assert response.status_code == 200
    assert response.json() == {"filename": "blob.bin", "size": len(payload)}


def test_upload_empty_file_returns_size_zero():
    client = TestClient(app7)
    response = client.post("/upload/", files={"file": ("empty.txt", b"", "text/plain")})
    assert response.status_code == 200
    assert response.json() == {"filename": "empty.txt", "size": 0}


def test_upload_without_file_returns_422():
    client = TestClient(app7)
    response = client.post("/upload/")
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "file"]

# 在下方编写你的代码实现
if __name__ == "__main__":
    # 运行测试：pytest test_file.py
    pass