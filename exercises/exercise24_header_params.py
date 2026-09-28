# 练习24：Header参数
# 
# 学习目标：
# 1. 导入并使用 Header
# 2. 声明 Header 参数
# 3. 理解下划线到连字符的自动转换
# 4. 处理重复的 Header

# TODO: 导入必要的模块
from typing import Annotated
from fastapi import FastAPI, Header, Query, Path

# TODO: 创建 FastAPI 应用实例
app = FastAPI()

# TODO: 创建一个简单的 Header 参数端点
# 路径: /items/
# Header 参数: user_agent (可选的 str)
# 返回: {"User-Agent": user_agent}
# 注意：参数名 user_agent 会自动转换为 User-Agent
@app.get("/items/")
def get_item(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

# TODO: 创建一个带必需 Header 的端点
# 路径: /auth/
# Header 参数: authorization (必需的 str)
# 返回: {"authorization": authorization}
@app.get("/auth/")
def get_auth(authorization: Annotated[str, Header()]):
    return {"authorization": authorization}

# TODO: 创建一个带 Header 验证的端点
# 路径: /api/
# Header 参数:
#   - x_api_key (str，可选，最大长度: 50)
#   - x_request_id (str，可选，添加正则验证)
# 返回: {"x_api_key": x_api_key, "x_request_id": x_request_id}
@app.get("/api/")
def get_api(
    x_api_key: Annotated[str | None, Header(max_length=50)] = None,
    x_request_id: Annotated[str | None, Header(pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")] = None
):
    return {"x_api_key": x_api_key, "x_request_id": x_request_id}

# TODO: 创建一个禁用下划线转换的端点
# 路径: /special/
# Header 参数: strange_header (str，可选，禁用 convert_underscores)
# 返回: {"strange_header": strange_header}
@app.get("/special/")
def get_special(strange_header: Annotated[str | None, Header(convert_underscores=False)] = None):
    return {"strange_header": strange_header}

# TODO: 创建一个处理重复 Header 的端点
# 路径: /tokens/
# Header 参数: x_token (list[str]，可选)
# 返回: {"X-Token values": x_token}
# 测试：发送多个 X-Token header
@app.get("/tokens/")
def get_tokens(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}

# TODO: 创建一个混合参数类型的端点
# 路径: /request/{request_id}
# 路径参数: request_id (int)
# 查询参数: verbose (bool，可选)
# Header 参数: 
#   - x_client_version (str，可选)
#   - accept_language (str，可选)
# 返回: 包含所有参数的字典
@app.get("/request/{request_id}")
def get_request(
    request_id: Annotated[int, Path()],
    verbose: Annotated[bool | None, Query()] = None,
    x_client_version: Annotated[str | None, Header()] = None,
    accept_language: Annotated[str | None, Header()] = None
):
    return {"request_id": request_id, "verbose": verbose, "x_client_version": x_client_version, "accept_language": accept_language}

# TODO: 创建一个带多个标准 Header 的端点
# 路径: /headers/
# Header 参数:
#   - content_type (可选的 str)
#   - accept (可选的 str)
#   - host (可选的 str)
# 返回: 包含所有 header 值的字典
@app.get("/headers/")
def get_headers(
    content_type: Annotated[str | None, Header()] = None,
    accept: Annotated[str | None, Header()] = None,
    host: Annotated[str | None, Header()] = None
):
    return {"content_type": content_type, "accept": accept, "host": host}

if __name__ == "__main__":
    pass
