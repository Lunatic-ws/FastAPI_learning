# 练习30：表单数据处理
# 要求：创建接收表单数据的接口

from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, status

app = FastAPI()
# 题目：
# 1. 创建一个POST接口 /login，接收username和password表单字段
#    - username: 最少3个字符
#    - password: 最少6个字符
#    - 返回包含username和登录状态的JSON响应
#
# 2. 创建一个POST接口 /register，接收注册表单数据
#    - username: 必填，最少3个字符
#    - email: 必填
#    - password: 必填，最少6个字符
#    - age: 可选，整数类型
#    - 验证两次密码是否一致
#    - 返回注册成功的用户信息
#
# 3. 创建一个POST接口 /update-profile，支持部分字段更新
#    - name: 必填
#    - nickname: 可选
#    - bio: 可选，默认为空字符串
#    - 返回更新后的用户信息
#
@app.post("/login")
def login(
    username: Annotated[str, Form(min_length=3)],
    password: Annotated[str, Form(min_length=6)],
) -> dict:
    return {"username": username, "message": "登录成功"}

@app.post("/register")
def register(
    username: Annotated[str, Form(min_length=3)],
    email: Annotated[str, Form()],
    password: Annotated[str, Form(min_length=6)],
    password_confirm: Annotated[str, Form(min_length=6)],
    age: Annotated[int | None, Form()] = None,
) -> dict:
    if password != password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="两次输入的密码不一致"
        )
    return {
        "message": "注册成功",
        "user": {"username": username, "email": email, "age": age},
    }

@app.post("/update-profile")
def update_profile(
    name: Annotated[str, Form()],
    nickname: Annotated[str | None, Form()] = None,
    bio: Annotated[str, Form()] = "",
) -> dict:
    return {"name": name, "nickname": nickname, "bio": bio}
# 提示：
# - 使用 Form() 声明表单参数
# - 使用 Form(min_length=3) 添加验证
# - 使用 Optional[str] 和 Form(default=None) 声明可选字段
#
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
