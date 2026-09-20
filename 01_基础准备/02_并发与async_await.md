# 并发与async/await（Concurrency and async/await）

## 学习目标
- 理解同步与异步编程的区别
- 掌握async/await语法
- 了解asyncio基本使用
- 理解FastAPI中的异步处理机制

## 为什么需要异步编程

### 同步 vs 异步

**同步（阻塞）**：代码按顺序执行，每个操作必须等待上一个操作完成
```python
import time

def synchronous_task():
    print("开始任务1")
    time.sleep(2)  # 阻塞2秒
    print("任务1完成")
    
    print("开始任务2")
    time.sleep(2)  # 又阻塞2秒
    print("任务2完成")
    
# 总共需要4秒
synchronous_task()
```

**异步（非阻塞）**：多个任务可以并发执行，不必等待
```python
import asyncio

async def asynchronous_task():
    print("开始任务1")
    await asyncio.sleep(2)  # 非阻塞，可以切换到其他任务
    print("任务1完成")
    
    print("开始任务2")
    await asyncio.sleep(2)
    print("任务2完成")

async def main():
    # 并发执行两个任务
    await asyncio.gather(
        asynchronous_task(),
        asynchronous_task()
    )
    
# 总共只需约2秒（并发执行）
asyncio.run(main())
```

## async/await语法

### async定义协程

```python
# async def 定义的函数是协程（coroutine）
async def say_hello():
    print("Hello!")
    return "greeting"

# 调用协程函数不会立即执行，而是返回协程对象
coro = say_hello()
print(type(coro))  # <class 'coroutine'>

# 需要用await执行
async def main():
    result = await say_hello()
    print(result)  # "greeting"

asyncio.run(main())
```

### await等待协程

```python
async def fetch_data(url):
    print(f"从 {url} 获取数据...")
    await asyncio.sleep(1)  # 模拟网络请求
    return f"{url}的数据"

async def main():
    # await会暂停当前协程，等待操作完成
    data1 = await fetch_data("https://api1.com")
    data2 = await fetch_data("https://api2.com")
    print(data1, data2)

asyncio.run(main())
```

## 并发执行

### asyncio.gather

```python
async def fetch_all():
    # 并发执行多个协程
    results = await asyncio.gather(
        fetch_data("https://api1.com"),
        fetch_data("https://api2.com"),
        fetch_data("https://api3.com")
    )
    return results

# 三个请求并发执行，总时间约1秒而不是3秒
```

### asyncio.create_task

```python
async def with_tasks():
    # 创建任务（立即开始执行）
    task1 = asyncio.create_task(fetch_data("https://api1.com"))
    task2 = asyncio.create_task(fetch_data("https://api2.com"))
    
    # 可以做其他事情
    print("任务已创建，正在执行...")
    
    # 等待任务完成
    result1 = await task1
    result2 = await task2
    
    return result1, result2
```

## 何时使用异步

### 适合异步的场景
- **网络I/O**：HTTP请求、数据库查询
- **文件I/O**：读写大文件
- **等待操作**：sleep、等待用户输入

### 不适合异步的场景
- **CPU密集型计算**：图像处理、机器学习
- **简单脚本**：开销大于收益

## FastAPI中的异步

### 异步路径操作

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/async-endpoint")
async def async_endpoint():
    # 可以使用await
    data = await fetch_data_from_db()
    return {"data": data}

@app.get("/sync-endpoint")
def sync_endpoint():
    # 普通同步函数
    data = fetch_data_sync()
    return {"data": data}
```

### 异步数据库示例

```python
from fastapi import FastAPI
from databases import Database

app = FastAPI()
database = Database("sqlite:///test.db")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    query = "SELECT * FROM users WHERE id = :user_id"
    return await database.fetch_one(query, values={"user_id": user_id})
```

## 练习题

### 练习1：基础async/await
**文件位置**: `exercises/exercise4_async_basic.py`

```python
import asyncio

# TODO: 将以下同步函数改为异步函数
def wait_and_print(seconds, message):
    print(f"等待 {seconds} 秒...")
    time.sleep(seconds)  # 改用 asyncio.sleep
    print(message)
    return message

async def main():
    # TODO: 并发调用两次 wait_and_print
    # 第一次等待2秒，打印"First"
    # 第二次等待1秒，打印"Second"
    # 应该总共只等待约2秒
    pass

if __name__ == "__main__":
    asyncio.run(main())
```

### 练习2：并发请求模拟
**文件位置**: `exercises/exercise5_async_concurrent.py`

```python
import asyncio
import random

async def fetch_url(url: str) -> dict:
    """模拟异步HTTP请求"""
    delay = random.uniform(0.5, 2.0)
    print(f"开始获取: {url}")
    await asyncio.sleep(delay)
    print(f"完成获取: {url} (耗时 {delay:.2f}s)")
    return {"url": url, "delay": delay}

async def main():
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/posts",
        "https://api.example.com/comments",
        "https://api.example.com/albums",
    ]
    
    # TODO: 使用 asyncio.gather 并发获取所有URL
    # 记录开始时间
    # 获取所有结果
    # 记录结束时间
    # 打印总耗时
    
    pass

if __name__ == "__main__":
    asyncio.run(main())
```

### 练习3：异步任务管理
**文件位置**: `exercises/exercise6_async_tasks.py`

```python
import asyncio

async def background_task(name: str, duration: int):
    """后台任务"""
    print(f"任务 {name} 开始，预计运行 {duration} 秒")
    await asyncio.sleep(duration)
    print(f"任务 {name} 完成")
    return f"{name}_result"

async def main():
    # TODO: 创建3个任务并分别管理
    # task1: "A", 运行3秒
    # task2: "B", 运行1秒
    # task3: "C", 运行2秒
    
    # 使用 asyncio.create_task 创建任务
    
    # 在等待任务完成前，打印"所有任务已创建"
    
    # 等待所有任务完成并收集结果
    
    pass

if __name__ == "__main__":
    asyncio.run(main())
```

### 练习4：FastAPI异步端点
**文件位置**: `exercises/exercise7_fastapi_async.py`

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

# TODO: 创建一个异步数据库模拟
async def fake_db_query(query: str, delay: float = 1.0):
    """模拟数据库查询"""
    await asyncio.sleep(delay)
    return {"query": query, "result": "data"}

# TODO: 创建以下端点

# GET /users/{user_id}
# 异步查询用户，模拟延迟0.5秒

# GET /posts/{post_id}
# 异步查询文章，模拟延迟0.3秒

# GET /combined/{user_id}/{post_id}
# 并发查询用户和文章，返回组合结果

# 启动命令: uvicorn exercise7_fastapi_async:app --reload
```

## 运行练习

```bash
python exercises/exercise4_async_basic.py
python exercises/exercise5_async_concurrent.py
python exercises/exercise6_async_tasks.py
uvicorn exercises.exercise7_fastapi_async:app --reload
```

## 完成后告知我检查批改！

## 参考资源
- [Python asyncio文档](https://docs.python.org/3/library/asyncio.html)
- [FastAPI并发文档](https://fastapi.tiangolo.com/async/)
