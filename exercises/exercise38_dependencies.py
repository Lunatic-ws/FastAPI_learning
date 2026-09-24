# 练习38：依赖注入
# 要求：学习创建和使用依赖、共享依赖、层级依赖

# 题目1：基本依赖注入
# 创建依赖函数common_params，接收查询参数：
# - q: str | None = None
# - skip: int = 0
# - limit: int = 100
# 返回字典包含这些参数
# 创建路径 GET /items/ 和 GET /users/
# 使用Depends注入common_params
# 返回注入的依赖结果
# 提示：commons: Annotated[dict, Depends(common_params)]

# 题目2：共享Annotated依赖
# 创建依赖函数get_pagination，接收page和size参数（默认1和10）
# 创建类型别名PaginationDep = Annotated[dict, Depends(get_pagination)]
# 在多个路径操作中使用这个类型别名：
# - GET /products/
# - GET /orders/
# - GET /customers/
# 所有路径都返回注入的分页参数

# 题目3：依赖作为类
# 创建类CommonQueryParams：
# - __init__接收q: str | None = None, skip: int = 0, limit: int = 100
# - 存储为实例属性
# 在路径操作中使用Depends(CommonQueryParams)
# 提示：FastAPI会自动实例化类

# 题目4：依赖返回Pydantic模型
# 创建Pydantic模型User：
# - id: int
# - username: str
# - email: str
# 创建依赖函数get_current_user，返回User实例（模拟认证用户）
# 创建路径 GET /profile/，注入User依赖
# 返回用户信息
# 提示：user: User = Depends(get_current_user)

# 题目5：层级依赖（子依赖）
# 创建依赖函数get_db，返回数据库连接字符串（模拟）
# 创建依赖函数get_user_repo，依赖get_db，返回仓库对象
# 创建依赖函数get_current_user，依赖get_user_repo，返回当前用户
# 创建路径 GET /me/，注入get_current_user依赖
# 返回用户信息
# 提示：层级关系：get_db -> get_user_repo -> get_current_user

# 题目6：依赖中的异常处理
# 创建依赖函数verify_token，接收查询参数token
# 如果token为None或不是"secret"，抛出HTTPException(401, "Invalid token")
# 如果有效，返回{"user_id": 123}
# 创建路径 GET /protected/，注入verify_token依赖
# 返回受保护的数据
# 测试：不带token或错误token应返回401

# 题目7：全局依赖
# 创建依赖函数require_api_key，检查头部X-API-Key
# 如果不存在或不等于"my-api-key"，抛出HTTPException(403)
# 使用app = FastAPI(dependencies=[Depends(require_api_key)])添加全局依赖
# 创建多个路径操作，所有路径都需要API key
# 提示：所有路径都会自动应用这个依赖

# 题目8：依赖中的yield（资源清理）
# 创建依赖函数get_db_connection，使用yield返回数据库连接
# 在yield之前：创建连接
# 在yield之后：关闭连接（打印"Connection closed"）
# 创建路径 GET /data/，注入依赖
# 返回{"data": "from database"}
# 提示：使用try/finally确保清理

# 题目9：路径操作装饰器中的依赖
# 创建依赖函数verify_admin，检查用户是否为管理员
# 创建路径 POST /admin/users/，在装饰器中添加依赖：
# @app.post("/admin/users/", dependencies=[Depends(verify_admin)])
# 不在函数参数中注入，只在装饰器中声明
# 返回{"created": true}
# 提示：装饰器中的依赖不返回值，只执行验证

# 题目10：综合练习 - 完整认证系统
# 实现完整的认证依赖层级：
# 1. get_db：数据库连接（yield）
# 2. get_token_from_header：从Authorization头部提取token
# 3. verify_token：验证token有效性（依赖get_token_from_header）
# 4. get_current_user：获取当前用户（依赖verify_token和get_db）
# 5. require_active_user：验证用户是否激活（依赖get_current_user）
# 创建以下路径操作：
# - POST /login/：接收username和password，返回token
# - GET /profile/：需要认证，返回用户信息（依赖get_current_user）
# - GET /admin/：需要管理员权限（依赖require_active_user并检查is_admin）
# - PUT /settings/：需要认证，更新用户设置（依赖get_current_user）
# 提示：使用字典模拟数据库和token存储

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
