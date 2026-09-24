# 练习50：后台任务
# 要求：学习使用BackgroundTasks、创建后台任务函数、依赖注入中使用后台任务

# 题目1：基本后台任务
# 创建函数write_log，接收message参数，写入文件"app.log"
# 创建路径 POST /log/{message}，添加后台任务执行write_log
# 返回{"message": "Log scheduled"}
# 测试：访问后检查app.log文件内容
# 提示：background_tasks.add_task(write_log, message)

# 题目2：发送邮件模拟
# 创建函数send_email，接收email和content参数
# 模拟发送邮件：sleep(3)，打印"Email sent to {email}"
# 创建路径 POST /send-email/{email}，接收请求体包含content
# 添加后台任务发送邮件
# 立即返回{"message": "Email will be sent", "email": email}
# 提示：使用time.sleep模拟慢操作

# 题目3：处理文件
# 创建函数process_file，接收filename参数
# 模拟文件处理：sleep(5)，写入处理结果到"processed_{filename}.txt"
# 创建路径 POST /upload/{filename}，接收文件内容（字符串）
# 添加后台任务处理文件
# 返回{"status": "Processing started", "filename": filename}，状态码202
# 提示：返回时使用status_code=202

# 题目4：多个后台任务
# 创建三个函数：
# - task1：打印"Task 1 executed"
# - task2：打印"Task 2 executed"
# - task3：打印"Task 3 executed"
# 创建路径 POST /multi-tasks/，添加三个后台任务
# 返回{"message": "All tasks scheduled"}
# 测试：观察控制台输出顺序

# 题目5：后台任务带多个参数
# 创建函数generate_report，接收：
# - report_type: str
# - user_id: int
# - date_range: str
# 写入文件"report_{report_type}_{user_id}.txt"，包含所有参数信息
# 创建路径 POST /reports/，接收请求体包含这些参数
# 添加后台任务，传递所有参数
# 返回{"status": "Report generation started"}
# 提示：background_tasks.add_task(generate_report, report_type, user_id, date_range)

# 题目6：依赖注入中的后台任务
# 创建依赖函数log_request，接收BackgroundTasks参数
# 添加后台任务记录请求信息到"requests.log"
# 创建路径 GET /data/，注入依赖
# 返回{"data": "some data"}
# 提示：依赖函数可以接收BackgroundTasks参数

# 题目7：async任务函数
# 创建async函数async_task，使用await asyncio.sleep(2)
# 打印"Async task completed"
# 创建路径 POST /async-task/，添加后台任务
# 返回{"message": "Async task scheduled"}
# 提示：async def函数也可以作为后台任务

# 题目8：后台任务与数据库操作
# 创建函数save_to_db，接收data字典
# 模拟数据库操作：sleep(2)，打印"Saved to DB: {data}"
# 创建Pydantic模型Item：
# - name: str
# - price: float
# - quantity: int
# 创建路径 POST /items/，接收Item请求体
# 添加后台任务保存到数据库
# 立即返回{"status": "Item received", "item": item}
# 提示：传递item.dict()或item.model_dump()

# 题目9：后台任务异常处理
# 创建函数risky_task，可能抛出异常
# 使用try/except捕获异常并记录到"task_errors.log"
# 创建路径 POST /risky/，添加后台任务
# 返回{"message": "Task scheduled"}
# 提示：后台任务中的异常不会影响已返回的响应

# 题目10：综合练习 - 订单处理系统
# 实现完整的订单处理系统：
# 创建Pydantic模型Order：
# - order_id: str
# - customer_email: str
# - items: list[str]
# - total_amount: float
# 创建以下函数：
# - send_confirmation_email：发送确认邮件（sleep 2秒，打印）
# - update_inventory：更新库存（sleep 1秒，打印）
# - process_payment：处理支付（sleep 3秒，打印）
# - generate_invoice：生成发票，写入文件"invoice_{order_id}.txt"
# 创建路径 POST /orders/，接收Order请求体
# 添加四个后台任务
# 返回{"status": "Order accepted", "order_id": order_id}，状态码202
# 测试：访问后观察控制台输出和生成的发票文件

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
