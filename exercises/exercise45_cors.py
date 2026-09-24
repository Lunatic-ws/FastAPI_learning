# 练习45：CORS跨域资源共享
# 要求：学习配置CORS、理解源的概念、处理跨域请求

# 题目1：基本CORS配置
# 创建FastAPI应用
# 配置CORS中间件，允许以下源：
# - "http://localhost:3000"
# - "http://localhost:8080"
# - "https://example.com"
# 允许所有方法和头部
# 创建路径 GET /api/data/，返回{"data": "This is API data"}
# 提示：使用app.add_middleware(CORSMiddleware, ...)

# 题目2：允许所有源
# 创建FastAPI应用
# 配置CORS中间件，使用allow_origins=["*"]允许所有源
# 允许所有方法和头部
# 创建路径 GET /public/info/，返回{"info": "Public information"}
# 注意：这种方式不支持凭证（cookies、authorization headers等）

# 题目3：支持凭证的CORS
# 创建FastAPI应用
# 配置CORS中间件：
# - allow_origins：显式指定源列表（不能使用"*"）
# - allow_credentials=True
# - allow_methods：显式指定方法列表（不能使用"*"）
# - allow_headers：显式指定头部列表（不能使用"*"）
# 创建路径 GET /user/profile/，返回{"user": "authenticated user"}
# 提示：当allow_credentials=True时，不能使用通配符

# 题目4：限制HTTP方法
# 创建FastAPI应用
# 配置CORS中间件，只允许GET和POST方法
# 允许特定源："http://localhost:3000"
# 创建路径：
# - GET /items/：返回{"items": []}
# - POST /items/：接收JSON数据，返回{"created": true}
# - DELETE /items/{item_id}/：删除项目
# 测试：DELETE请求应被CORS阻止

# 题目5：使用正则表达式匹配源
# 创建FastAPI应用
# 配置CORS中间件，使用allow_origin_regex匹配：
# - 所有https://开头的子域名，如：https://.*\.example\.com
# 允许所有方法和头部
# 创建路径 GET /api/test/，返回{"status": "ok"}
# 提示：allow_origin_regex='https://.*\.example\.com'

# 题目6：暴露自定义头部
# 创建FastAPI应用
# 配置CORS中间件：
# - 允许源："http://localhost:3000"
# - 使用expose_headers=["X-Custom-Header", "X-Request-ID"]
# 创建路径 GET /custom/，添加两个响应头部：
# - "X-Custom-Header": "custom-value"
# - "X-Request-ID": "12345"
# 返回{"message": "check headers"}
# 提示：使用response.headers["X-Custom-Header"] = "custom-value"

# 题目7：设置最大缓存时间
# 创建FastAPI应用
# 配置CORS中间件：
# - 允许源："http://localhost:3000"
# - max_age=3600（缓存CORS响应1小时）
# 创建路径 GET /cached/，返回{"cached": "response"}
# 提示：max_age单位是秒

# 题目8：综合练习 - 完整CORS配置
# 创建FastAPI应用，模拟生产环境配置：
# 配置CORS中间件：
# - 允许的源：从环境变量读取（提供默认值列表）
# - 允许凭证
# - 允许的方法：["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
# - 允许的头部：["*"]
# - 暴露的头部：["X-Total-Count", "X-Page-Count"]
# - 最大缓存时间：86400秒（24小时）
# 创建多个路径操作：
# - GET /api/products/：返回产品列表，添加头部"X-Total-Count"
# - POST /api/products/：创建产品
# - PUT /api/products/{product_id}/：更新产品
# - DELETE /api/products/{product_id}/：删除产品
# 提示：使用import os读取环境变量，os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
