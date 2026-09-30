# 练习47：大型应用结构
#
# 目标：使用APIRouter组织大型应用
#
# 任务：
# 1. 创建一个主应用文件 main.py
# 2. 创建 routers/users.py 路由模块，包含 GET /users/ 和 GET /users/{user_id}
# 3. 创建 routers/items.py 路由模块，包含 GET /items/ 和 POST /items/
# 4. 使用 include_router() 将路由模块包含到主应用
#
# 提示：
# - 使用 APIRouter() 创建路由器
# - 可以设置 prefix、tags、dependencies 参数
# - 子模块需要 from fastapi import APIRouter
# - 主应用需要 from .routers import users, items

from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    email: str | None = None


class Item(BaseModel):
    id: int
    name: str
    price: float


def verify_token(x_token: Annotated[str, Header()]) -> str:
    if x_token != "fake-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token validation failed"
        )
    return x_token


users: list[User] = [
    User(id=1, username="alice", email="alice@example.com"),
    User(id=2, username="bob"),
]

items: list[Item] = [
    Item(id=1, name="Hammer", price=9.99),
    Item(id=2, name="Nail", price=0.5),
]

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_token)],
)


@users_router.get("/")
def read_users() -> list[User]:
    return users


@users_router.get("/{user_id}")
def read_user(user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )


items_router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(verify_token)],
)


@items_router.get("/")
def read_items() -> list[Item]:
    return items


@items_router.post("/")
def create_item(item: Item) -> Item:
    item.id = max((existing.id for existing in items), default=0) + 1
    items.append(item)
    return item


app.include_router(users_router)
app.include_router(items_router)

if __name__ == "__main__":
    pass
