# 练习5：并发请求模拟
# 要求：使用 asyncio.gather 并发执行多个异步任务
import asyncio
import random
import time
# 题目：并发获取所有URL，记录总耗时
urls = [
    "https://api.example.com/users",
    "https://api.example.com/posts",
    "https://api.example.com/comments",
    "https://api.example.com/albums",
]
#
# 要求：
# 1. 记录开始时间
# 2. 使用 asyncio.gather 并发获取所有URL
# 3. 记录结束时间
# 4. 打印总耗时和所有结果
#
# 提示：可以使用以下异步函数模拟HTTP请求
async def fetch_url(url: str) -> dict:
    """模拟异步HTTP请求"""
    delay = random.uniform(0.5, 2.0)
    print(f"开始获取: {url}")
    await asyncio.sleep(delay)
    print(f"完成获取: {url} (耗时 {delay:.2f}s)")
    return {"url": url, "delay": delay}

async def main():
    start = time.time()
    results = await asyncio.gather(*[fetch_url(url) for url in urls])
    end = time.time()
    runtime = end - start
    print(f"\n总耗时：{runtime:.2f}s")
    print(f"结果：{results}")

# 在下方编写你的代码实现
if __name__ == "__main__":
    asyncio.run(main())