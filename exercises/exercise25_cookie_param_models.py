# 练习25：Cookie参数模型
# 要求：根据注释要求实现相应的FastAPI应用

# 题目1：使用模型接收Cookie参数
# 创建Cookies模型(BaseModel): session_id(str), favorite_number(可选int), interest(可选str)
# 使用 Annotated[Cookies, Cookie()] 声明Cookie参数
# 创建GET接口 /items/ 返回收到的Cookies内容

# 题目2：验证与默认值
# 为session_id添加 Field(min_length=8) 验证
# 为favorite_number添加 Field(ge=0, le=100) 范围验证
# 使用浏览器开发者工具或 curl -b "session_id=abc12345" 发送Cookie测试
# 验证不通过时观察422错误的返回

# 题目3：观察OpenAPI文档
# 访问 /docs 查看Cookie参数模型在文档中的展示方式
# 使用文档中的 Try it out 带上Cookie测试接口

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
