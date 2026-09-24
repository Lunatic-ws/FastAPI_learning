# 练习60：自定义Response类（Custom Response Class）
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 使用ORJSONResponse
要求:
- pip install orjson 后，创建应用设置 default_response_class=ORJSONResponse
- （未安装时在注释中记录该配置方式即可）
- 创建一个返回大量嵌套数据的接口，对比orjson的转义/性能特点（注释回答）
"""

"""
任务2: 使用UJSONResponse
要求:
- 创建GET接口 /ujson/
- 使用 response_class=UJSONResponse
- （注释说明：需要 pip install ujson，ujson不那么严格，是"最优努力"模式）
"""

"""
任务3: 自定义XMLResponse
要求:
- 创建XMLResponse类继承Response，media_type="application/xml"
- 创建GET接口 /xml/ 返回简单的XML内容
"""

"""
任务4: 覆盖优先级
要求:
- 应用级设置default_response_class
- 单个路由显式设置response_class
- 在注释中回答：路由级和应用级配置哪个生效
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
