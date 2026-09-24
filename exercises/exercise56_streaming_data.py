# 练习56：流式数据（Streaming Response）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 同步生成器流式响应
要求:
- 使用 StreamingResponse 配合同步生成器
- 生成器逐个产出数字0-9，每个数字带换行符
- 创建GET接口 /stream-sync/ 返回流式结果
"""

"""
任务2: 异步生成器流式响应
要求:
- 使用 async def 生成器，asyncio.sleep(0.5) 模拟耗时产出
- 逐秒产出当前时间字符串，共产出5次
- 创建GET接口 /stream-async/
"""

"""
任务3: 大文件分块返回
要求:
- 模拟一个1MB的bytes数据
- 实现 iter_file(data, chunk_size=65536) 生成器按块产出
- 创建GET接口 /download/ 用 StreamingResponse 返回，media_type="application/octet-stream"
- 添加 Content-Disposition 响应头模拟文件下载
"""

"""
任务4: 流式JSON
要求:
- 创建GET接口 /stream-json/
- 使用生成器逐行产出 json.dumps 的对象（如 {"value": n}）
- 设置正确的 media_type
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
