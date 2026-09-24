# 练习31：表单模型
# 要求：根据注释要求实现相应的FastAPI应用
# 说明：表单需要 python-multipart 支持

# 题目1：用Pydantic模型声明表单字段
# 创建LoginForm模型(BaseModel): username(str), password(str)
# 使用 Annotated[LoginForm, Form()] 声明表单参数
# 创建POST接口 /login/ 返回 {"username": ..., "password": ...}

# 题目2：模型字段验证
# 为password添加 Field(min_length=8) 验证
# 为username添加 Field(pattern=r"^[a-zA-Z0-9_]+$") 限制字符
# 测试不符合验证的数据返回422

# 题目3：模型与普通Form字段混用
# 创建POST接口 /register/
# 同时使用表单模型和一个独立的普通Form字段(如 captcha: str = Form(...))
# 观察两者在 /docs 中的展示方式是否一致

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
