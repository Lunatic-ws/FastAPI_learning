# 练习：路径参数
# 目标：使用路径参数创建动态路由
from fastapi import FastAPI

app = FastAPI()
# 任务：
# 1. 创建 GET /users/{user_id} 路由，user_id 为 int 类型
# 2. 返回 {"user_id": user_id, "type": "int"}
# 3. 创建 GET /items/{item_name} 路由，item_name 为 str 类型
# 4. 返回 {"item_name": item_name, "length": len(item_name)}
# 提示：
# - 路径参数用 {参数名} 格式
# - 函数参数需添加类型注解
# - FastAPI 会自动验证和转换类型
@app.get("/users/{user_id}")
def get_userid(user_id: int):
    return {"user_id": user_id, "type": "int"}
@app.get("/items/{item_name}")
def get_itemname(item_name: str):
    return {"item_name": item_name, "length": len(item_name)}

if __name__ == "__main__":
    pass
