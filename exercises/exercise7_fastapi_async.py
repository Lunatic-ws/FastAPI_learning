# 练习7：FastAPI异步端点
# 要求：创建异步FastAPI端点，实现并发查询
from fastapi import FastAPI
import asyncio

app = FastAPI()

# 提示：可以使用以下模拟数据库查询函数
async def fake_db_query(query: str, delay: float = 1.0):
    """模拟数据库查询"""
    await asyncio.sleep(delay)
    return {"query": query, "result": "data"}
# 题目1：创建 GET /users/{user_id} 端点
# 要求：异步查询用户，延迟0.5秒
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    result = await fake_db_query(f"select * from users where id = {user_id}",0.5)
    return {"user_id": user_id, "data": result}

# 题目2：创建 GET /posts/{post_id} 端点
# 要求：异步查询文章，延迟0.3秒
@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    result = await fake_db_query(f"select * from posts where id = {post_id}",0.3)
    return {"post_id": post_id, "data": result}

# 题目3：创建 GET /combined/{user_id}/{post_id} 端点
# 要求：并发查询用户和文章，返回组合结果
# 提示：使用 asyncio.gather 同时查询两个资源
@app.get("/combined/{user_id}/{post_id}")
async def get_combined(user_id: int, post_id:int):
    result_user, result_post = await asyncio.gather(
        fake_db_query(f"select * from users where id = {user_id}", 0.5),
        fake_db_query(f"select * from posts where id = {post_id}", 0.3)
    )

    return {"user": result_user, "post": result_post}

# 在下方编写你的代码实现
# 启动命令: uvicorn exercise7_fastapi_async:app --reload
async def main():
    pass

if __name__ == "__main__":
    pass
