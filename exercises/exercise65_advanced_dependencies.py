# 练习65: 高级依赖注入
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 参数化依赖 - 实现可调用类
要求:
- 创建一个类 QueryChecker，通过 __init__ 接收一个字符串 pattern
- 实现 __call__ 方法，接收查询参数 text: str，检查 text 是否包含 pattern
- 创建两个实例: email_checker 和 phone_checker
- email_checker 检查是否包含 "@"
- phone_checker 检查是否包含数字
- 创建两个路由 /check-email/ 和 /check-phone/，分别使用这两个依赖
- 返回布尔值表示是否匹配
"""

"""
任务2: 参数化依赖 - 实现验证器类
要求:
- 创建一个 RangeValidator 类
- __init__ 接收 min_value 和 max_value
- __call__ 接收参数 value: int，验证是否在范围内
- 如果不在范围内，抛出 HTTPException
- 创建实例 age_validator (范围: 0-150) 和 score_validator (范围: 0-100)
- 创建路由 /validate-age/ 和 /validate-score/ 使用这些依赖
"""

"""
任务3: 带yield的依赖 - 数据库会话模拟
要求:
- 创建一个 MockDatabase 类，有 connect() 和 disconnect() 方法
- 实现 get_db() 依赖，使用 yield 返回数据库连接
- 在 yield 前调用 connect()，yield 后调用 disconnect()
- 创建路由 /users/ 使用该依赖，返回用户列表
- 打印日志验证连接和断开的调用顺序
"""

"""
任务4: 带yield和scope的依赖
要求:
- 实现 get_resource() 依赖，使用 yield 返回资源对象
- 资源对象有 acquire() 和 release() 方法
- 测试两种 scope:
  - 使用 Depends(get_resource, scope="function")
  - 使用 Depends(get_resource, scope="request")
- 创建两个路由对比行为差异
- 打印日志观察资源获取和释放的时机
"""

"""
任务5: 依赖工厂模式
要求:
- 创建一个 DependencyFactory 类
- 提供 create_auth_dependency(permission: str) 方法，返回不同的权限验证依赖
- create_auth_dependency 返回的依赖函数会检查用户是否有指定权限
- 实现模拟用户系统，用户有 permissions 列表
- 创建路由 /admin/ 要求 "admin" 权限，/editor/ 要求 "editor" 权限
"""

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
