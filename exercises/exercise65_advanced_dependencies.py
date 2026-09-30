# 练习65: 高级依赖注入
# 本练习文件只有注释，请在下方编写代码实现

from typing import Annotated, Any

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Security, status
from fastapi.security import SecurityScopes

app = FastAPI()

"""
任务1: 参数化依赖 - 实现可调用类
要求:
- 创建一个类 QueryChecker，通过 __init__ 接收一个字符串 pattern
- 实现 __call__ 方法，接收查询参数 text: str，检查 text 是否包含 pattern
- 创建两个实例: email_checker 和 phone_checker
- email_checker 检查是否包含 "@"
- phone_checker 检查是否包含数字
- 创建两个路由 /check-email/ 和 /check-phone/，分别使用这两个依赖
- 返回布尔值表示是否匹配
"""


class QueryChecker:
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def __call__(self, text: str) -> bool:
        return any(character in text for character in self.pattern)


email_checker = QueryChecker("@")
phone_checker = QueryChecker("0123456789")


@app.get("/check-email/")
def check_email(matched: Annotated[bool, Depends(email_checker)]) -> dict[str, Any]:
    return {"matched": matched, "pattern": email_checker.pattern}


@app.get("/check-phone/")
def check_phone(matched: Annotated[bool, Depends(phone_checker)]) -> dict[str, Any]:
    return {"matched": matched, "pattern": phone_checker.pattern}

"""
任务2: 参数化依赖 - 实现验证器类
要求:
- 创建一个 RangeValidator 类
- __init__ 接收 min_value 和 max_value
- __call__ 接收参数 value: int，验证是否在范围内
- 如果不在范围内，抛出 HTTPException
- 创建实例 age_validator (范围: 0-150) 和 score_validator (范围: 0-100)
- 创建路由 /validate-age/ 和 /validate-score/ 使用这些依赖
"""


class RangeValidator:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, value: int = Query(...)) -> int:
        if not self.min_value <= value <= self.max_value:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"value must be between {self.min_value} and {self.max_value}",
            )
        return value


age_validator = RangeValidator(min_value=0, max_value=150)
score_validator = RangeValidator(min_value=0, max_value=100)


@app.get("/validate-age/")
def validate_age(value: Annotated[int, Depends(age_validator)]) -> dict[str, int]:
    return {"value": value, "min": age_validator.min_value, "max": age_validator.max_value}


@app.get("/validate-score/")
def validate_score(value: Annotated[int, Depends(score_validator)]) -> dict[str, int]:
    return {"value": value, "min": score_validator.min_value, "max": score_validator.max_value}

"""
任务3: 带yield的依赖 - 数据库会话模拟
要求:
- 创建一个 MockDatabase 类，有 connect() 和 disconnect() 方法
- 实现 get_db() 依赖，使用 yield 返回数据库连接
- 在 yield 前调用 connect()，yield 后调用 disconnect()
- 创建路由 /users/ 使用该依赖，返回用户列表
- 打印日志验证连接和断开的调用顺序
"""


class MockDatabase:
    def __init__(self) -> None:
        self.connected = False

    def connect(self) -> "MockDatabase":
        print("[db] connect")
        self.connected = True
        return self

    def disconnect(self) -> None:
        print("[db] disconnect")
        self.connected = False

    def query_users(self) -> list[dict[str, Any]]:
        return [
            {"id": 1, "username": "alice"},
            {"id": 2, "username": "bob"},
        ]


def get_db() -> Any:
    database = MockDatabase()
    database.connect()
    try:
        yield database
    finally:
        database.disconnect()


@app.get("/users/")
def read_users(database: Annotated[MockDatabase, Depends(get_db)]) -> dict[str, Any]:
    return {"connected": database.connected, "users": database.query_users()}

"""
任务4: 带yield和scope的依赖
要求:
- 实现 get_resource() 依赖，使用 yield 返回资源对象
- 资源对象有 acquire() 和 release() 方法
- 测试两种 scope:
  - 使用 Depends(get_resource, scope="function")
  - 使用 Depends(get_resource, scope="request")
- 创建两个路由对比行为差异
- 打印日志观察资源获取和释放的时机
"""


class MockResource:
    def __init__(self, name: str) -> None:
        self.name = name
        self.acquired = False

    def acquire(self) -> "MockResource":
        print(f"[resource:{self.name}] acquire")
        self.acquired = True
        return self

    def release(self) -> None:
        print(f"[resource:{self.name}] release")
        self.acquired = False

    def describe(self) -> str:
        return f"{self.name}:{'acquired' if self.acquired else 'released'}"


def get_resource() -> Any:
    resource = MockResource("shared").acquire()
    try:
        yield resource
    finally:
        resource.release()


@app.get("/resource/function-scope/")
def resource_function_scope(
    resource: Annotated[MockResource, Depends(get_resource, scope="function")],
) -> dict[str, str]:
    return {"state": resource.describe()}


@app.get("/resource/request-scope/")
def resource_request_scope(
    resource: Annotated[MockResource, Depends(get_resource, scope="request")],
) -> dict[str, str]:
    return {"state": resource.describe()}


class HitCounter:
    def __init__(self) -> None:
        self.hits = 0

    def __call__(self) -> int:
        self.hits += 1
        return self.hits


hit_counter = HitCounter()


@app.get("/cache-demo/")
def cache_demo(
    cached: Annotated[int, Depends(hit_counter)],
    fresh: Annotated[int, Depends(hit_counter, use_cache=False)],
) -> dict[str, int]:
    return {"cached": cached, "fresh": fresh}

"""
任务5: 依赖工厂模式
要求:
- 创建一个 DependencyFactory 类
- 提供 create_auth_dependency(permission: str) 方法，返回不同的权限验证依赖
- create_auth_dependency 返回的依赖函数会检查用户是否有指定权限
- 实现模拟用户系统，用户有 permissions 列表
- 创建路由 /admin/ 要求 "admin" 权限，/editor/ 要求 "editor" 权限
"""

fake_users: dict[str, dict[str, Any]] = {
    "root": {"username": "root", "permissions": ["admin", "editor"]},
    "writer": {"username": "writer", "permissions": ["editor"]},
    "guest": {"username": "guest", "permissions": []},
}


def get_current_user(
    security_scopes: SecurityScopes,
    x_user: Annotated[str | None, Header()] = None,
) -> dict[str, Any]:
    username = x_user if x_user is not None else (security_scopes.scopes[0] if security_scopes.scopes else "guest")
    user = fake_users.get(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


class DependencyFactory:
    @staticmethod
    def create_auth_dependency(permission: str) -> Any:
        def dependency(
            user: Annotated[dict[str, Any], Security(get_current_user, scopes=[permission])],
        ) -> dict[str, Any]:
            if permission not in user["permissions"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"需要 {permission} 权限",
                )
            return user

        dependency.__name__ = f"require_{permission}"
        return dependency


require_admin = DependencyFactory.create_auth_dependency("admin")
require_editor = DependencyFactory.create_auth_dependency("editor")


@app.get("/admin/")
def admin_panel(
    user: Annotated[dict[str, Any], Security(require_admin, scopes=["admin"])],
) -> dict[str, Any]:
    return {"user": user["username"], "panel": "admin"}


@app.get("/editor/")
def editor_panel(
    user: Annotated[dict[str, Any], Security(require_editor, scopes=["editor"])],
) -> dict[str, Any]:
    return {"user": user["username"], "panel": "editor"}


protected_router = APIRouter(dependencies=[Depends(require_admin)])


@protected_router.get("/reports/")
def read_reports() -> dict[str, str]:
    return {"report": "quarterly"}


app.include_router(protected_router, prefix="/protected", tags=["protected"])

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)