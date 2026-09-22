# 练习12：查询参数
# 目标：使用查询参数实现过滤和分页
from fastapi import FastAPI

app = FastAPI()
# 任务：
# 1. 创建 GET /items/ 路由，包含查询参数 skip（int，默认0）和 limit（int，默认10）
# 2. 返回 {"skip": skip, "limit": limit, "items": ["item1", "item2", ...]}
# 3. items 列表根据 skip 和 limit 返回对应数量的项目
# 4. 创建 GET /users/{user_id} 路由，包含可选查询参数 detail（bool，默认False）
# 5. 如果 detail=True，返回完整用户信息；否则返回简要信息
# 提示：
# - 查询参数通过函数参数声明（非路径参数）
# - 默认值决定参数是否必需
# - bool 类型会自动转换 "true"/"false"/"1"/"0" 等
@app.get("/items/")
def get_item(skip: int = 0, limit: int = 10):
    all_items = [f"item{i}" for i in range(1,101)] # 假设有100个item
    items = all_items[skip : skip + limit]
    return {"skip": skip, "limit": limit, "items": items}
@app.get("/users/{user_id}")
def get_user(user_id: int, detail: bool = False):
    if detail:
        return {"user_id": user_id, "detail": []}
    return {"user_id": user_id}

if __name__ == "__main__":
    pass
