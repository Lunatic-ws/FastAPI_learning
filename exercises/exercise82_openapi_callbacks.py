# 练习82：OpenAPI回调（OpenAPI Callbacks）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 定义回调模型
要求:
- 创建Invoice模型: id(str), title(可选str), customer(str), total(float)
- 创建InvoiceEvent模型: description(str), paid(bool)
- 创建InvoiceEventReceived模型: ok(bool)
"""

"""
任务2: 声明回调路由
要求:
- 创建callbacks_router = APIRouter()
- 用 @callbacks_router.post(...) 声明回调端点：
  接收InvoiceEvent，返回InvoiceEventReceived
- 路径中使用 {invoice_id} 占位符
"""

"""
任务3: 关联回调到接口
要求:
- 创建POST /invoices/ 接口，接收Invoice
- 在装饰器中使用 callbacks=callbacks_router.name
- （提示：将callbacks_router作为参数注册到APIRouter/FastAPI，并引用其回调函数）
- 访问/docs查看Callbacks部分的展示
"""

"""
任务4: 回调的意义
要求:
- 在注释中回答：回调与普通接口的区别（谁调用谁）
- 举一个装修行业SaaS中适合用回调的业务场景
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
