# 练习33：表单与文件
# 要求：根据注释要求实现相应的FastAPI应用

# 题目1：同时接收文件和表单字段
# 创建POST接口 /files/
# 接收 file: UploadFile 和 note: str = Form(...)
# 返回文件名和备注信息

# 题目2：多文件与多表单字段组合
# 创建POST接口 /upload-multiple/
# 接收 files: list[UploadFile] 和 tags: list[str] = Form([])
# 返回文件数量和标签列表

# 题目3：表单模型与文件组合
# 定义UploadMeta模型(BaseModel): author(str), category(可选str)
# 使用 Annotated[UploadMeta, Form()] 与 UploadFile 同时接收
# 在 /docs 中查看表单模型字段的展示效果

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
