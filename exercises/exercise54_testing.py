# 练习54：测试
# 要求：使用TestClient为FastAPI应用编写测试

# 题目1：基础测试
# 创建以下应用并编写测试：
# - GET /：返回{"message": "Welcome"}
# - GET /health：返回{"status": "ok"}
# 测试两个路径的status_code和json内容


# 题目2：测试路径参数
# 创建以下应用并编写测试：
# - GET /items/{item_id}：返回{"item_id": item_id}
# 测试：
# - item_id为1时返回正确结果
# - item_id为"abc"时返回正确结果


# 题目3：测试查询参数
# 创建以下应用并编写测试：
# - GET /users/：接受skip和limit参数，返回{"skip": skip, "limit": limit}
# 测试：
# - 默认参数值
# - 自定义参数值


# 题目4：测试请求体
# 创建以下应用并编写测试：
# - POST /items/：接受Item模型（name: str, price: float）
# 测试：
# - 正常创建
# - 缺少必填字段返回422错误


# 题目5：测试Headers和错误
# 创建以下应用并编写测试：
# - GET /protected/：需要X-API-Key header
# - key正确返回{"status": "authorized"}
# - key错误返回401错误
# 测试：
# - 正确header
# - 错误header
# - 缺少header


# 题目6：测试表单数据
# 创建以下应用并编写测试：
# - POST /login/：接受username和password表单数据
# - 返回{"username": username, "logged_in": True}
# 测试表单提交


# 题目7：测试文件上传
# 创建以下应用并编写测试：
# - POST /upload/：接受文件上传
# - 返回{"filename": filename, "size": size}
# 测试文件上传


# 在下方编写你的代码实现
if __name__ == "__main__":
    # 运行测试：pytest test_file.py
    pass
