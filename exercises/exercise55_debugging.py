# 练习55：调试
# 要求：学习如何配置和使用调试器调试FastAPI应用

# 题目1：创建可调试的FastAPI应用
# 创建一个FastAPI应用，包含以下内容：
# - 在文件中直接调用uvicorn.run()
# - 使用if __name__ == "__main__"保护
# - GET /：返回{"message": "Hello World"}
# - GET /items/{item_id}：返回{"item_id": item_id}
# 在代码中设置断点，使用调试器调试


# 题目2：调试复杂逻辑
# 创建一个FastAPI应用，包含以下端点：
# - POST /calculate/：接受两个数字a和b
# - 计算a + b, a - b, a * b, a / b
# - 返回所有计算结果
# 在计算过程中设置断点，观察变量值


# 题目3：调试异步函数
# 创建一个包含异步端点的FastAPI应用：
# - async GET /async-data/：模拟异步操作（使用asyncio.sleep）
# - 返回{"message": "Async data"}
# 在异步函数中设置断点进行调试


# 题目4：调试异常处理
# 创建一个FastAPI应用，包含：
# - GET /divide/{a}/{b}：返回a / b的结果
# - 捕获ZeroDivisionError并返回自定义错误
# 在异常处理代码中设置断点


# 题目5：调试依赖注入
# 创建一个包含依赖注入的FastAPI应用：
# - 创建一个依赖函数get_db()
# - GET /users/：使用依赖获取"数据库连接"
# - 返回用户列表
# 在依赖函数和端点中设置断点


# 在下方编写你的代码实现
if __name__ == "__main__":
    # 使用调试器运行此文件
    pass
