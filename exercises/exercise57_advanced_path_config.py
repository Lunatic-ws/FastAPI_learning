# 练习57：路径操作高级配置（Response Class）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 返回纯文本
要求:
- 创建GET接口 /plain/
- 使用 response_class=PlainTextResponse 返回纯文本"Hello Plain"
- 对比不设置response_class时返回JSON的差异
"""

"""
任务2: 返回HTML
要求:
- 创建GET接口 /html/
- 使用 response_class=HTMLResponse 直接返回一段HTML字符串（如<h1>标题</h1>）
- 用浏览器或curl -i 观察Content-Type变化
"""

"""
任务3: 应用级默认响应类
要求:
- 创建FastAPI应用时设置 default_response_class=ORJSONResponse
- （注释说明：ORJSONResponse需要 pip install orjson，未安装时可改用UJSONResponse）
- 创建两个接口：一个使用应用默认，一个显式覆盖为PlainTextResponse
"""

"""
任务4: media_type观察
要求:
- 创建3个接口分别返回JSON/纯文本/HTML
- 用curl -i 查看各自响应头中的content-type并记录在注释中
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
