# 练习11：查询参数
# 要求：使用FastAPI实现以下API端点
from fastapi import FastAPI

app = FastAPI()
# 题目1：创建带有默认值的查询参数
# GET /products/
# 查询参数：
#   - skip: int = 0
#   - limit: int = 10
# 返回 {"skip": skip, "limit": limit, "products": ["product1", "product2"]}
@app.get("/products/")
def get_products(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit, "products": ["product1", "product2"]}

# 题目2：创建可选查询参数
# GET /search/
# 查询参数：
#   - q: str | None = None (可选搜索关键词)
#   - category: str | None = None (可选分类)
# 如果q存在，返回 {"query": q, "category": category, "results": [...]}
# 如果q不存在，返回 {"message": "No search query provided"}
@app.get("/search/")
def get_result(q: str | None = None, category: str | None = None):
    if q:
        return {"query": q, "category": category, "results": ["result1", "result2"]}
    return {"message": "No search query provided"}

# 题目3：bool类型查询参数
# GET /users/{user_id}
# 路径参数：user_id: str
# 查询参数：detailed: bool = False
# 如果 detailed 为 True，返回完整用户信息
# 如果 detailed 为 False，返回简化用户信息
@app.get("/users/{user_id}")
def get_user(user_id: str, detailed: bool = False):
    if detailed:
        return {"user_id": user_id, "details": []}
    return {"user_id": user_id}

# 题目4：必需查询参数
# GET /calculate/
# 查询参数：
#   - x: float (必需)
#   - y: float (必需)
#   - operation: str = "add" (默认值)
# 根据operation执行相应计算（add, subtract, multiply, divide）
# 返回 {"x": x, "y": y, "operation": operation, "result": result}
@app.get("/calculate/")
def calculate_result(x: float, y: float, operation: str = "add"):
    if operation == "add":
        return {"x": x, "y": y, "operation": operation, "result": x + y}
    elif operation == "subtract":
        return {"x": x, "y": y, "operation": operation, "result": x - y}
    elif operation == "multiply":
        return {"x": x, "y": y, "operation": operation, "result": x * y}
    elif operation == "divide":
        if y == 0:
            return {"error": "Cannot divide by zero"}
        return {"x": x, "y": y, "operation": operation, "result": x / y}
    else:
        return {"error": "Invalid operation"}

# 题目5：混合路径参数和查询参数
# GET /departments/{dept_id}/employees/
# 路径参数：dept_id: int
# 查询参数：
#   - skip: int = 0
#   - limit: int = 10
#   - active_only: bool = True
# 返回 {"department_id": dept_id, "skip": skip, "limit": limit, "active_only": active_only, "employees": [...]}
@app.get("/departments/{dept_id}/employees/")
def get_dept(dept_id: int, skip: int = 0, limit: int = 10, active_only: bool = True):
    return {"department_id": dept_id, "skip": skip, "limit": limit, "active_only": active_only, "employees": []}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
