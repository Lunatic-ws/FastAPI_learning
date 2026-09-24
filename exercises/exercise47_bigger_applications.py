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

if __name__ == "__main__":
    pass
