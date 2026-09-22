# 练习9：路径参数
# 要求：使用FastAPI实现以下API端点
from fastapi import FastAPI, Path
from enum import Enum

app = FastAPI()
# 题目1：创建一个基本路径参数端点
# GET /items/{item_id}
# 返回 {"item_id": item_id, "message": "Item retrieved successfully"}
# item_id 必须是整数类型
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "message": "Item retrieved successfully"}

# 题目2：创建一个带类型验证的路径参数端点
# GET /users/{user_id}
# user_id 必须是整数
# 如果 user_id 小于 1，返回 {"error": "Invalid user ID"}
# 否则返回 {"user_id": user_id, "status": "active"}
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id < 1:
        return {"error": "Invalid user ID"}
    else:
        return {"user_id": user_id, "status": "active"}


# 题目3：使用Enum限制路径参数的可能值
# 创建枚举 ItemType，包含三种类型：book, movie, music
# GET /catalog/{item_type}
# 根据不同的 item_type 返回不同的消息
# book: {"type": "book", "section": "Library"}
# movie: {"type": "movie", "section": "Cinema"}
# music: {"type": "music", "section": "Music Store"}
class ItemType(Enum):
    book = "book"
    movie = "movie"
    music = "music"
    # ItemType.book表示ItemType.book
    # ItemType.book.name表示"book"（前）
    # ItemType.book.value表示"book"（后）

@app.get("/catalog/{item_type}")
def get_item(item_type: ItemType):
    if item_type == ItemType.book:
        return {"type": "book", "section": "Library"}
    elif item_type == ItemType.movie:
        return {"type": "movie", "section": "Cinema"}
    elif item_type == ItemType.music:
        return {"type": "music", "section": "Music Store"}


# 题目4：处理路径参数顺序问题
# 创建两个端点：
# GET /orders/latest - 返回 {"order_id": "latest", "items": 0}
# GET /orders/{order_id} - 返回 {"order_id": order_id}
# 注意：必须保证 /orders/latest 不被 /orders/{order_id} 匹配
@app.get("/orders/latest")
def get_order_latest():
    return {"order_id": "latest", "items": 0}
@app.get("/orders/{order_id}")
def get_order(order_id: str):
    return {"order_id": order_id}

# 题目5：路径参数包含路径
# GET /files/{file_path:path}
# 返回 {"file_path": file_path, "type": "file"}
# 测试URL: /files/documents/projects/myproject/main.py
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path, "type": "file"}

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    uvicorn.run(app, host="0.0.0.0", port=8000)
