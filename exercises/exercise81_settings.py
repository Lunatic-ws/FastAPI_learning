# 练习81：设置与环境变量（Settings and Environment Variables）
# 说明：需要 pip install pydantic-settings
# 本练习文件只有注释，请在下方编写代码实现

"""
任务1: 定义Settings类
要求:
- 创建Settings类继承BaseSettings
- 字段：app_name(str), admin_email(str), items_per_page(int=10)
- 使用 env_prefix="APP_" 使环境变量形如APP_ADMIN_EMAIL
"""

"""
任务2: .env文件
要求:
- 创建.env文件写入几个变量
- Settings的model_config中设置 env_file=".env"
- 实例化并打印配置，验证读取成功
"""

"""
任务3: lru_cache缓存的依赖
要求:
- 使用 @lru_cache 装饰 get_settings() 函数
- 作为依赖注入到接口中，返回app_name
- 在注释中回答：为什么需要lru_cache（提示：避免每次请求重新读环境变量）
"""

"""
任务4: 测试中覆盖配置
要求:
- 使用 app.dependency_overrides[get_settings] 返回修改后的Settings
- 测试接口返回的是覆盖后的配置
- 测试结束后清理overrides
"""
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
