# 练习73：位于代理后（Behind a Proxy）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 理解root_path
要求:
- 创建应用，启动时设置 root_path="/api/v1"
- （启动命令示例：uvicorn main:app --root-path /api/v1）
- 在注释中回答：root_path影响实际路由匹配吗，还是只影响文档
"""

"""
任务2: 代理转发头
要求:
- 在注释中回答以下问题：
  - 代理服务器通常会改写哪些请求头（X-Forwarded-For / X-Forwarded-Proto）
  - 应用如何拿到客户端真实IP
- 创建GET接口 /client-info/ 尝试返回请求头中的x-forwarded-for
"""

"""
任务3: 文档路径
要求:
- 设置root_path后，访问 /api/v1/docs 与 /docs 的区别
- 在注释中记录：docs页面中Try it out请求的前缀变化
"""

"""
任务4: 常见问题排查
要求:
- 在注释中列出至少3种"位于代理后"的典型问题（如文档加载失败、重定向丢失前缀）
- 每个问题写出1条排查思路
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
