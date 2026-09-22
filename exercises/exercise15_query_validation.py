# 练习15：查询参数验证
# 要求：根据每个题目的要求，使用 Query 和 Annotated 实现验证功能
from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import AfterValidator

app = FastAPI()
# 题目1：基础长度验证
# 创建一个 GET /search/ 接口
# - 查询参数 keyword：可选，最大长度 20，最小长度 2
# - 返回 {"keyword": keyword, "results": []}
# 如果 keyword 不符合长度要求，FastAPI 应自动返回错误
@app.get("/search/")
def get_search(keyword: Annotated[str | None, Query(max_length=20, min_length=2)] = None):
    return {"keyword": keyword, "results":[]}

# 题目2：正则表达式验证
# 创建一个 GET /users/ 接口
# - 查询参数 username：可选，只允许字母、数字和下划线，长度 3-20
# - 正则提示：使用 pattern="^[a-zA-Z0-9_]{3,20}$"
# - 返回 {"username": username}
@app.get("/users/")
def get_user(username: Annotated[str | None, Query(min_length = 3,max_length=20,pattern="^[a-zA-Z0-9_]{3,20}$")] = None):
    return {"username": username}

# 题目3：必需参数验证
# 创建一个 GET /validate/ 接口
# - 查询参数 code：必需，必须以 "CODE-" 开头，后面跟至少 3 位数字
# - 正则提示：pattern="^CODE-\d{3,}$"
# - 返回 {"code": code, "valid": True}
@app.get("/validate/")
def get_validate(code: Annotated[str, Query(pattern="^CODE-\d{3,}$")]):
    return {"code": code, "valid": True}

# 题目4：多值查询参数
# 创建一个 GET /filter/ 接口
# - 查询参数 tags：可选，可以接收多个值（列表）
# - 默认值为 ["python", "fastapi"]
# - URL 示例：/filter/?tags=python&tags=web
# - 返回 {"tags": tags}
@app.get("/filter/")
def get_filter(tags: Annotated[list[str], Query()] = ["python", "fastapi"]):
    return {"tags": tags}

# 题目5：别名和元数据
# 创建一个 GET /items/ 接口
# - 查询参数 q：
#   - 别名：item-query（URL 中使用 item-query）
#   - 标题："Search Query"
#   - 描述："Search items by query string"
#   - 最大长度：50
#   - 可选
# - 返回 {"query": q}
@app.get("/items/")
def get_item(q: Annotated[str | None, Query(alias="item-query", title="Search Query", description="Search items by query string", max_length=50)] = None):
    return {"query": q}

# 题目6：自定义验证器
# 创建一个 GET /books/ 接口
# - 查询参数 isbn：可选
# - 使用 AfterValidator 验证：
#   - 必须以 "ISBN-" 开头
#   - 后面必须是 10 或 13 位数字
# - 提示：自定义验证函数 check_isbn
# - 返回 {"isbn": isbn, "valid": True}
def check_isbn(isbn):
    if isbn is None:
        return None
    if not isbn.startswith("ISBN-"):
        raise ValueError("error")
    digits = isbn[5:]
    if len(digits) not in (10, 13) or not digits.isdigit():
        raise ValueError("error")
    return isbn

@app.get("/books/")
def get_book(isbn: Annotated[str | None, AfterValidator(check_isbn)] = None):
    return {"isbn": isbn, "valid": True}

# 题目7：弃用参数
# 创建一个 GET /legacy/ 接口
# - 查询参数 old_param：
#   - 已弃用（deprecated=True）
#   - 描述："This parameter is deprecated, use new_param instead"
# - 查询参数 new_param：可选，最大长度 30
# - 返回 {"old_param": old_param, "new_param": new_param}
@app.get("/legacy/")
def get_legacy(
    old_param: Annotated[str | None, Query(description = "This parameter is deprecated, use new_param instead",deprecated = True)] = None,
    new_param: Annotated[str | None, Query(max_length = 30)] = None
):
    return {"old_param": old_param, "new_param": new_param}

# 题目8：综合练习
# 创建一个 GET /products/ 接口，包含以下查询参数：
# - name: 可选，最小长度 2，最大长度 100，标题 "Product Name"
# - category: 可选，必须为 "electronics"、"books"、"clothing" 之一（使用 pattern）
# - min_price: 可选，别名 "min-price"
# - max_price: 可选，别名 "max-price"
# - tags: 可选，多值列表，默认值 ["featured"]
# - sort: 已弃用，描述 "Use 'ordering' instead"
# - 返回所有参数的值
@app.get("/products/")
def get_products(
    name: Annotated[str | None, Query(min_length = 2, max_length = 100,title = "Product Name")] = None,
    category: Annotated[str | None, Query(pattern = "^(electronics|books|clothing)$")] = None,
    min_price: Annotated[str | None, Query(alias = "min-price")] = None,
    max_price: Annotated[str | None, Query(alias = "max-price")] = None,
    tags: Annotated[list[str] | None, Query()] = ["featured"],
    sort: Annotated[str | None, Query(deprecated = True, description="Use 'ordering' instead")] = None
):
    return {
        "name": name, 
        "category": category, 
        "min_price": min_price, 
        "max_price": max_price,
        "tags": tags,
        "ordering": sort
        }

# 在下方编写你的代码实现
if __name__ == "__main__":
    pass
