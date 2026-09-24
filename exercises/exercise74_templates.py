# 练习74：模板（Templates）
# 说明：需要 pip install jinja2
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 配置Jinja2Templates
要求:
- 创建templates目录并新建 hello.html（包含 {{ name }} 变量）
- 实例化 templates = Jinja2Templates(directory="templates")
"""

"""
任务2: 返回模板响应
要求:
- 创建GET接口 /hello/{name}
- 使用 templates.TemplateResponse(request=request, name="hello.html", context={"name": name})
- 用浏览器访问查看渲染结果
"""

"""
任务3: 模板中的逻辑与url_for
要求:
- 在hello.html中使用 {% for %} 渲染一个列表
- 在context中传入应用的路由路径，或使用 request.url_path
- 创建一个包含简单表格展示的页面
"""

"""
任务4: 模板与API共存
要求:
- 同一应用中既有返回JSON的API接口，又有返回HTML的模板接口
- 在注释中回答：这类"多页面+API"结构适合什么项目形态
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
