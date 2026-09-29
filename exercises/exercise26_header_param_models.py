# 练习26：Header参数模型
# 要求：根据注释要求实现相应的FastAPI应用
from fastapi import FastAPI, Header
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()
# 题目1：使用模型接收Header参数
# 创建CommonHeaders模型(BaseModel): host(str), save_data(bool可选), if_modified_since(可选str)
# 使用 Annotated[CommonHeaders, Header()] 声明Header参数
# 创建GET接口 /items 返回收到的Headers内容
# 注意: Python变量名中的下划线会自动转换为Header中的连字符
class CommonHeaders(BaseModel):
    host: str
    save_data: bool | None = None
    if_modified_since: str | None = None

@app.get("/items")
def get_item(commonheader: Annotated[CommonHeaders, Header()]):
    return commonheader

# 题目2：验证与必填控制
# 为host添加 Field(min_length=3) 验证
# 将save_data设为必填bool，测试缺少该Header时的422错误
# 使用curl -H "save-data: true" 测试布尔值转换
class CommonHeaders2(BaseModel):
    host: str = Field(min_length=3)
    save_data: bool
    if_modified_since: str | None = None

@app.get("/items2")
def get_item2(commonheader: Annotated[CommonHeaders2, Header()]):
    return commonheader

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
