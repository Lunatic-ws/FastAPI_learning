# 练习61：OpenAPI额外响应（Additional Responses in OpenAPI）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 声明带模型的额外响应
要求:
- 创建Message模型: message(str)
- 创建GET接口 /items/{item_id}
- responses={404: {"model": Message, "description": "条目不存在"}}
- 404时抛出HTTPException，观察/docs中该响应的文档展示
"""

"""
任务2: 同一状态码返回多种media_type
要求:
- 在responses中使用内容字典格式：
  "200": {"content": {"image/png": {}, "application/json": {}}}
- 在注释中说明这种写法在文档中的展示效果
"""

"""
任务3: 额外响应与默认响应共存
要求:
- 接收int参数（天然有422），同时声明自定义404
- 观察/docs中422和404是否都展示
"""

"""
任务4: description与example
要求:
- 为额外响应添加description和example字段
- 在/docs中查看示例是否显示
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
