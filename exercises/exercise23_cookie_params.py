# 练习23：Cookie参数
# 
# 学习目标：
# 1. 导入并使用 Cookie
# 2. 声明 Cookie 参数
# 3. 为 Cookie 参数添加验证
# 4. 理解 Cookie 参数与查询参数的区别

# TODO: 导入必要的模块
from typing import Annotated
from fastapi import FastAPI, Cookie

# TODO: 创建 FastAPI 应用实例
app = FastAPI()

# TODO: 创建一个简单的 Cookie 参数端点
# 路径: /items/
# Cookie 参数: ads_id (可选的 str)
# 返回: {"ads_id": ads_id}
@app.get("/items/")
def get_item(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
# TODO: 创建一个带必需 Cookie 的端点
# 路径: /user/
# Cookie 参数: session_id (必需的 str)
# 返回: {"session_id": session_id}

# TODO: 创建一个带 Cookie 验证的端点
# 路径: /settings/
# Cookie 参数:
#   - theme: str (可选，默认值 "light"，可选值: "light", "dark", "auto")
#   - language: str (可选，默认值 "en"，最大长度: 5)
# 返回: {"theme": theme, "language": language}

# TODO: 创建一个带多个 Cookie 参数的端点
# 路径: /preferences/
# Cookie 参数:
#   - user_id: int (可选)
#   - tracking_enabled: bool (可选，默认值 True)
#   - last_visit: str (可选)
# 返回: 包含所有 Cookie 值的字典

# TODO: 创建一个混合参数类型的端点
# 路径: /analytics/{page_id}
# 路径参数: page_id (int)
# 查询参数: timestamp (可选的 str)
# Cookie 参数: visitor_id (可选的 str)
# 返回: 包含所有参数的字典

# TODO: 创建一个带 Cookie 说明的端点
# 路径: /config/
# Cookie 参数: 
#   - config_token (str，可选，添加描述 "Configuration token for user preferences")
# 返回: {"config_token": config_token}

if __name__ == "__main__":
    pass
