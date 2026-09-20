# 练习6：异步任务管理
# 要求：使用 asyncio.create_task 创建和管理异步任务
import asyncio
# 题目：创建3个任务并管理它们
# 要求：
# 1. 创建3个任务：
#    - task1: 名称"A", 运行3秒
#    - task2: 名称"B", 运行1秒
#    - task3: 名称"C", 运行2秒
# 2. 使用 asyncio.create_task 创建任务
# 3. 在等待任务完成前，打印"所有任务已创建"
# 4. 等待所有任务完成并收集结果
# 5. 打印所有结果
#
# 提示：可以使用以下后台任务函数
async def background_task(name: str, duration: int):
    """后台任务"""
    print(f"任务 {name} 开始，预计运行 {duration} 秒")
    await asyncio.sleep(duration)
    print(f"任务 {name} 完成")
    return f"{name}_result"

async def main():
    task1 = asyncio.create_task(background_task("A", 3))
    task2 = asyncio.create_task(background_task("B", 1))
    task3 = asyncio.create_task(background_task("C", 2))

    print("所有任务已创建")

    result1 = await task1
    result2 = await task2
    result3 = await task3
    print(f"结果：{result1}，{result2}，{result3}")

# 在下方编写你的代码实现
if __name__ == "__main__":
    asyncio.run(main())
