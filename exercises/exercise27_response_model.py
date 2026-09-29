# 练习27: 响应模型
# 要求：根据注释要求实现相应的FastAPI应用
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

app = FastAPI()
# 题目1: 基础响应模型
# 创建一个POST接口 /items
# Item模型: name(str), description(可选str), price(float), tags(list[str],默认[])
# 使用返回类型注解声明响应模型
# 返回接收到的item
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tags: list[str] = []
@app.post("/items")
def post_item(item: Item) -> Item:
    return item

# 题目2: 列表响应模型
# 创建一个GET接口 /items
# 返回类型: list[Item]
# Item模型: name(str), price(float)
# 返回包含2个Item的列表
class Item2(BaseModel):
    name: str
    price: float
@app.get("/items")
def get_item() -> list[Item2]:
    return [Item2(name="a", price=2.5), Item2(name="b", price=3.2)]

# 题目3: 密码过滤（安全）
# 创建UserIn模型: username(str), password(str), email(str)
# 创建UserOut模型: username(str), email(str)
# 创建一个POST接口 /users
# 接收UserIn，使用response_model=UserOut返回
# 确保password不会出现在响应中
class UserIn(BaseModel):
    username: str
    password: str
    email: str
class UserOut(BaseModel):
    username: str
    email: str
@app.post("/users", response_model=UserOut)
def post_user(userin: UserIn) -> Any:
    return userin

# 题目4: 模型继承
# 创建BaseUser模型: username(str), email(str), full_name(可选str)
# 创建UserIn模型继承BaseUser，添加password(str)
# 创建一个POST接口 /users/inherit
# 接收UserIn，返回类型注解为BaseUser
# 确保编辑器不报错，且password被过滤
class BaseUser(BaseModel):
    username: str
    email: str
    full_name: str | None = None
class UserIn2(BaseUser):
    password: str
@app.post("/users/inherit")
def post_inherit(user: UserIn2) -> BaseUser:
    return user

# 题目5: 排除未设置字段
# 创建Product模型: name(str), description(可选str), price(float), tax(float=10.5), tags(list[str]=[])
# 创建一个GET接口 /products/{product_id}
# 使用response_model_exclude_unset=True
# 创建products字典包含至少2个产品（一个只有必需字段，一个有可选字段）
# 观察返回结果的差异
class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

products = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2}
}

@app.get("/products/{product_id}", response_model_exclude_unset=True)
def get_product(product_id: str) -> Product:
    return products[product_id]

# 题目6: 包含/排除特定字段
# 创建Item模型: name(str), description(可选str), price(float), secret_code(str)
# 创建一个GET接口 /items/{item_id}/public
# 使用response_model_exclude排除secret_code字段
# 创建一个GET接口 /items/{item_id}/brief
# 使用response_model_include只包含name和price字段
class Item3(BaseModel):
    name: str
    description: str | None = None
    price: float
    secret_code: str

items = {
    "foo": {"name": "Foo", "description": "The foo", "price": 42.0, "secret_code": "s3cr3t"},
}

@app.get("/items/{item_id}/public", response_model_exclude={"secret_code"})
def get_item_public(item_id: str) -> Item3:
    return items[item_id]

@app.get("/items/{item_id}/brief",response_model_include={"name", "price"})
def get_item_brief(item_id: str) -> Item3:
    return items[item_id]

# 题目7: response_model与Any
# 创建Item模型: name(str), price(float)
# 创建一个POST接口 /items/any
# 接收Item，使用response_model=Item
# 返回类型注解为Any
# 返回一个字典（非Item对象），验证response_model会自动转换
class Item4(BaseModel):
    name: str
    price: float
@app.post("/items/any", response_model=Item4)
def post_any(item: Item4) -> Any:
    return {"name": item.name, "price": item.price}

# 题目8: 嵌套模型响应
# 创建Address模型: street(str), city(str), country(str)
# 创建User模型: name(str), age(int), address(Address)
# 创建一个GET接口 /users/{user_id}
# 返回类型为User
# 返回一个包含嵌套address的用户对象
class Address(BaseModel):
    street: str
    city: str
    country: str
class User(BaseModel):
    name: str
    age: int
    address: Address
@app.get("/users/{user_id}")
def get_user(user_id: int) -> User:
    return User(
        name="John",
        age=18,
        address=Address(
            street="123 St",
            city="B town",
            country="A"
        )    
    )

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
