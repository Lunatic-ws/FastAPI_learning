# 练习83：OpenAPI Webhooks
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 声明webhook
要求:
- 使用 @app.webhooks.post("/new-subscription") 声明webhook
- 接收Subscription模型: username(str), monthly_fee(float), start_date(datetime)
- 定义Invoice模型供另一个webhook使用
"""

"""
任务2: 多个webhook
要求:
- 再声明一个 @app.webhooks.post("/new-invoice")
- 访问 /docs 并查看页面上的Webhooks区域
- 在注释中记录：webhooks与普通接口在文档中的区别
"""

"""
任务3: webhook与callbacks的区别
要求:
- 在注释中回答以下问题：
  - webhooks：应用会在什么情况下向外部URL发起请求
  - callbacks：回调URL由谁在什么参数中提供
- 各举一个使用场景
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
