# 练习32：文件上传处理
# 要求：创建处理文件上传的接口
# 题目：
# 1. 创建一个POST接口 /upload，处理单文件上传
#    - 接收一个文件参数
#    - 返回文件名、文件类型、文件大小
#    - 使用UploadFile类型
#
# 2. 创建一个POST接口 /upload-multiple，处理多文件上传
#    - 接收多个文件（List[UploadFile]）
#    - 返回每个文件的文件名、类型、大小
#    - 返回总文件数和总大小
#
# 3. 创建一个POST接口 /upload-with-metadata，文件与表单混合
#    - 接收一个文件
#    - 接收description表单字段（必填）
#    - 接收tags表单字段（可选）
#    - 返回文件信息和元数据
#
# 4. 创建一个POST接口 /upload-image，验证图片文件
#    - 只接受图片文件（image/jpeg, image/png, image/gif）
#    - 最大文件大小限制为5MB
#    - 如果不符合要求，返回400错误
#    - 返回图片信息
#
# 5. 创建一个POST接口 /upload-and-save，保存文件到服务器
#    - 创建uploads目录存储文件
#    - 使用分块写入方式保存大文件
#    - 返回文件保存路径
#
# 提示：
# - 使用 UploadFile = File() 声明文件参数
# - 使用 List[UploadFile] = File() 声明多文件
# - 使用 await file.read() 异步读取文件内容
# - 使用 file.content_type 检查文件类型
# - 使用 Form() 添加表单字段
# - 使用 os.makedirs 创建目录
# - 使用分块写入处理大文件：while chunk := await file.read(1024*1024)
#
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
