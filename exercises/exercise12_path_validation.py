# 练习12：路径参数验证
# 要求：根据每个题目的要求，使用 Path 和 Annotated 实现验证功能
from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()
# 题目1：基础数值验证
# 创建一个 GET /items/{item_id} 接口
# - item_id：整数，必须大于等于 1
# - 返回 {"item_id": item_id}
# 测试：/items/1 有效，/items/0 无效
@app.get("/items/{item_id}")
def get_item_id(item_id: Annotated[int, Path(ge = 1)]):
    return {"item_id": item_id}

# 题目2：范围验证
# 创建一个 GET /users/{user_id} 接口
# - user_id：整数，必须在 1 到 1000 之间（包含边界）
# - 添加标题 "User ID" 和描述 "The unique identifier for the user"
# - 返回 {"user_id": user_id}
@app.get("/users/{user_id}")
def get_user_id(user_id: Annotated[int, Path(ge = 1, le = 1000, title="User ID", description="The unique identifier for the user")]):
    return {"user_id": user_id}

# 题目3：浮点数验证
# 创建一个 GET /temperature/{temp} 接口
# - temp：浮点数，必须大于 -273.15（绝对零度），小于等于 1000
# - 返回 {"temperature": temp, "unit": "celsius"}
@app.get("/temperature/{temp}")
def get_temp(temp: Annotated[float, Path(gt = -273.15, le = 1000)]):
    return {"temperature": temp, "unit": "celsius"}

# 题目4：组合路径和查询参数
# 创建一个 GET /items/{item_id} 接口
# - item_id：整数，必须大于 0
# - 查询参数 q：可选字符串，最大长度 50
# - 查询参数 size：可选浮点数，必须大于 0，小于 10.5
# - 返回包含所有参数的字典
@app.get("/item/{item_id}")
def get_item(item_id: Annotated[int, Path(gt = 0)],
             q: Annotated[str | None, Query(max_length = 50)] = None,
             size: Annotated[float | None, Query(gt = 0, lt = 10.5)] = None
):
    return {"item_id": item_id, "q": q, "size": size}

# 题目5：多个路径参数
# 创建一个 GET /users/{user_id}/items/{item_id} 接口
# - user_id：整数，必须大于等于 1
# - item_id：整数，必须大于等于 1，小于等于 100
# - 返回 {"user_id": user_id, "item_id": item_id}
@app.get("/users/{user_id}/items/{item_id}")
def get_userid_itemid(user_id: Annotated[int, Path(ge = 1)],
                      item_id: Annotated[int, Path(ge = 1, le = 100)]
):
    return {"user_id": user_id, "item_id": item_id}

# 题目6：页面验证
# 创建一个 GET /posts/{page} 接口
# - page：整数，必须在 1 到 1000 之间
# - 添加描述 "Page number for pagination"
# - 返回 {"page": page, "posts": [], "has_next": True}
@app.get("/posts/{page}")
def get_page(page: Annotated[int, Path(ge = 1, le = 1000, description = "Page number for pagination")]):
    return {"page": page, "posts": [], "has_next": True}

# 题目7：百分比验证
# 创建一个 GET /discount/{percentage} 接口
# - percentage：浮点数，必须大于等于 0，小于等于 100
# - 返回 {"discount_percentage": percentage, "valid": True}
@app.get("/discount/{percentage}")
def get_percentage(percentage: Annotated[float, Path(ge = 0, le = 100)]):
    return {"discount_percentage": percentage, "valid": True}

# 题目8：坐标验证
# 创建一个 GET /location/{lat}/{lon} 接口
# - lat（纬度）：浮点数，必须大于等于 -90，小于等于 90
# - lon（经度）：浮点数，必须大于等于 -180，小于等于 180
# - 返回 {"latitude": lat, "longitude": lon}
@app.get("/location/{lat}/{lon}")
def get_latandlon(
    lat: Annotated[float, Path(ge = -90, le = 90)],
    lon: Annotated[float, Path(ge = -180, le = 180)]
):
    return {"latitude": lat, "longitude": lon}

# 题目9：年份验证
# 创建一个 GET /events/{year} 接口
# - year：整数，必须在 1900 到 2100 之间
# - 查询参数 month：可选整数，必须在 1 到 12 之间（使用 Query）
# - 返回 {"year": year, "month": month}
@app.get("/events/{year}")
def get_year(
    year: Annotated[int, Path(ge = 1900, le = 2100)],
    month: Annotated[int | None, Query(ge = 1, le = 12)] = None
):
    return {"year": year, "month": month}

# 题目10：综合练习
# 创建一个 GET /products/{category_id}/{product_id} 接口
# - category_id：整数，必须大于等于 1，小于等于 100
# - product_id：整数，必须大于等于 1
# - 查询参数：
#   - name：可选字符串，最小长度 2，最大长度 100
#   - min_price：可选浮点数，必须大于等于 0
#   - max_price：可选浮点数，必须小于等于 10000
# - 返回包含所有参数的字典
@app.get("/products/{category_id}/{product_id}")
def get_product(
    category_id: Annotated[int, Path(ge = 1, le = 100)],
    product_id: Annotated[int, Path(ge = 1)],
    name: Annotated[str | None, Query(min_length = 2, max_length = 100)] = None,
    min_price: Annotated[float | None, Query(ge = 0)] = None,
    max_price: Annotated[float | None, Query(le = 10000)] = None
):
    return {"category_id": category_id, "product_id": product_id, "name": name, "min_price": min_price, "max_price": max_price}

# 在下方编写你的代码实现
if __name__ == "__main__":
    pass
