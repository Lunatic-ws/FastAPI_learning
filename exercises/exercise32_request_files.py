# 练习32：文件上传处理
# 要求：创建处理文件上传的接口

import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status

app = FastAPI()
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
@app.post("/upload")
async def upload_file(file: Annotated[UploadFile, File()]) -> dict:
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
    }

@app.post("/upload-multiple")
async def upload_files(files: Annotated[list[UploadFile], File()]) -> dict:
    file_details: list[dict] = []
    total_size = 0
    for file in files:
        content = await file.read()
        total_size += len(content)
        file_details.append(
            {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content),
            }
        )
    return {
        "files": file_details,
        "total_count": len(file_details),
        "total_size": total_size,
    }

@app.post("/upload-with-metadata")
async def upload_with_metadata(
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    tags: Annotated[list[str], Form()] = [],
) -> dict:
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "description": description,
        "tags": tags,
    }

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024

@app.post("/upload-image")
async def upload_image(file: Annotated[UploadFile, File()]) -> dict:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持 image/jpeg, image/png, image/gif 类型的图片",
        )
    content = await file.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="图片大小不能超过5MB"
        )
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "valid": True,
    }

UPLOAD_DIR = Path(tempfile.gettempdir()) / "uploads"

@app.post("/upload-and-save")
async def upload_and_save(file: Annotated[UploadFile, File()]) -> dict:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / (file.filename or "unnamed.bin")
    saved_size = 0
    with open(file_path, "wb") as target:
        while chunk := await file.read(1024 * 1024):
            target.write(chunk)
            saved_size += len(chunk)
    await file.close()
    return {
        "filename": file.filename,
        "size": saved_size,
        "path": str(file_path),
    }
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
