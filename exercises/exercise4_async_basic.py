# 练习4：基础async/await [已掌握]
# 要求：将同步函数改为异步函数，实现并发执行
import asyncio
# 题目1：将以下同步函数改为异步函数
# 提示：使用 async def 和 asyncio.sleep() 替代 time.sleep()
async def wait_and_print(seconds, message):
    print(f"等待 {seconds} 秒...")
    await asyncio.sleep(seconds)
    # 需要改为异步等待
    print(message)
    return message


# 题目2：并发调用两次 wait_and_print
# 第一次等待2秒，打印"First"
# 第二次等待1秒，打印"Second"
# 要求：总共只等待约2秒（并发执行）
async def main():
    # 使用 asyncio.gather 或 asyncio.create_task 实现并发
    # await asyncio.gather(
    #     wait_and_print(2, "First"),
    #     wait_and_print(1, "Second")
    # )
    task1 = asyncio.create_task(wait_and_print(2, "First"))
    task2 = asyncio.create_task(wait_and_print(1, "Second"))
    await task1
    await task2

# 在下方编写你的代码实现
if __name__ == "__main__":
    asyncio.run(main())
