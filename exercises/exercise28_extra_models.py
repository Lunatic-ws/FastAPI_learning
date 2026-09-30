# 练习28：额外模型

# 要求：
# 1. 定义三个用户模型：UserIn、UserOut、UserInDB
# 2. UserIn 包含：username, password, email, full_name(可选)
# 3. UserOut 不应包含密码
# 4. UserInDB 应包含 hashed_password 而非 password
# 5. 创建一个基类 UserBase 减少代码重复
# 6. 实现用户创建API：POST /users/
#    - 接收 UserIn
#    - 返回 UserOut
#    - 模拟保存到数据库（UserInDB）
# 7. 实现一个返回多种类型item的API：GET /items/{item_id}
#    - 可以返回 CarItem 或 PlaneItem
#    - 使用 Union 类型

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Literal

app = FastAPI()
# 题目1：定义模型基类和三个用户模型
# 使用继承，基类包含共享字段
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

# 题目2：实现密码哈希函数和用户保存函数
# fake_password_hasher(raw_password: str) -> str
# fake_save_user(user_in: UserIn) -> UserInDB
def fake_password_hasher(raw_password: str) -> str:
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn) -> UserInDB:
    return UserInDB(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=fake_password_hasher(user_in.password),
    )

# 题目3：创建用户API
# POST /users/
# 使用 response_model=UserOut
@app.post("/users/", response_model=UserOut)
def create_user(user_in: UserIn) -> Any:
    saved_user = fake_save_user(user_in)
    return saved_user

# 题目4：定义物品模型
# BaseItem, CarItem, PlaneItem
# CarItem 和 PlaneItem 继承 BaseItem
class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: Literal["car"] = "car"

class PlaneItem(BaseItem):
    type: Literal["plane"] = "plane"
    size: int

# 题目5：实现获取物品API
# GET /items/{item_id}
# 返回 Union[CarItem, PlaneItem]
# 预设一些测试数据
items = {
    "foo": {"description": "Foo item", "type": "car"},
    "bar": {"description": "Bar item", "type": "plane", "size": 5},
}

@app.get("/items/{item_id}", response_model=CarItem | PlaneItem)
def read_item(item_id: str) -> CarItem | PlaneItem:
    return items[item_id]

if __name__ == "__main__":
    pass
