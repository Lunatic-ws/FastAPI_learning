# 练习85：生成客户端（Generating a SDK/Client）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 导出OpenAPI规范
要求:
- 创建一个小型API应用（含Item模型和2个接口）
- 在注释中记录导出命令：
  - 启动后访问 http://127.0.0.1:8000/openapi.json 保存为文件
  - 或使用 python -c "import json; from main import app; print(json.dumps(app.openapi()))" > openapi.json
"""

"""
任务2: openapi-generator生成客户端
要求:
- 在注释中记录命令：
  npx @openapitools/openapi-generator-cli generate -i openapi.json -g typescript-fetch -o ./frontend-client
- 分别尝试生成 typescript-fetch 和 python 客户端
"""

"""
任务3: 使用生成的客户端
要求:
- 在注释中写出（或实际编写）使用生成客户端调用接口的示例代码
- 观察：生成的客户端中模型类与Pydantic模型的对应关系
"""

"""
任务4: 客户端与API同步
要求:
- 在注释中回答：后端修改模型后，前端如何最小成本地更新客户端代码
- 生成客户端相比手写fetch请求有哪些优势
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
