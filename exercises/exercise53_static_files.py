# 练习53：静态文件
# 要求：配置FastAPI应用提供静态文件服务

# 题目1：基本静态文件配置
# 创建一个FastAPI应用，挂载"static"目录到"/static"路径
# 目录结构提示：
# static/
#   - style.css
#   - script.js
#   - logo.png


# 题目2：多静态目录配置
# 配置三个静态文件目录：
# - "/static" -> directory="static" (公共静态资源)
# - "/uploads" -> directory="uploads" (用户上传文件)
# - "/assets" -> directory="assets" (前端资源)


# 题目3：版本化静态资源
# 为API的不同版本提供不同的静态文件目录：
# - "/v1/static" -> directory="static_v1"
# - "/v2/static" -> directory="static_v2"


# 题目4：条件挂载
# 根据环境变量决定是否挂载静态文件
# - 环境变量ENV为"development"时挂载
# - 其他环境不挂载


# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
