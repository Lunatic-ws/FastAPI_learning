# 练习25：Cookie参数模型
# 要求：根据注释要求实现相应的FastAPI应用
from fastapi import FastAPI, Cookie
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()
# 题目1：使用模型接收Cookie参数
# 创建Cookies模型(BaseModel): session_id(str), favorite_number(可选int), interest(可选str)
# 使用 Annotated[Cookies, Cookie()] 声明Cookie参数
# 创建GET接口 /items/ 返回收到的Cookies内容
class Cookies(BaseModel):
    session_id: str
    favorite_number: int | None = None
    interest: str | None = None

@app.get("/items")
def get_item(cookies: Annotated[Cookies, Cookie()]):
    return cookies

# 题目2：验证与默认值
# 为session_id添加 Field(min_length=8) 验证
# 为favorite_number添加 Field(ge=0, le=100) 范围验证
# 使用浏览器开发者工具或 curl -b "session_id=abc12345" 发送Cookie测试
# 验证不通过时观察422错误的返回
class Cookies2(BaseModel):
    session_id: str = Field(min_length=8)
    favorite_number: int | None = Field(default=None, ge=0, le=100)

@app.get("/items2")
def get_item2(cookies: Annotated[Cookies2, Cookie()]):
    return cookies

if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)