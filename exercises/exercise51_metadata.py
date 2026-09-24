# 练习51：Metadata和文档URLs
# 要求：为FastAPI应用添加元数据和自定义文档URL

# 题目1：创建一个FastAPI应用，包含完整的API元数据
# - 标题："电商平台API"
# - 描述：包含三个部分（产品管理、订单管理、用户管理）的描述（使用Markdown）
# - 摘要："电商平台的RESTful API"
# - 版本："1.0.0"
# - 服务条款URL："https://shop.example.com/terms"
# - 联系信息：name="API支持", email="support@shop.com"
# - 许可证：MIT（使用identifier）


# 题目2：为应用添加标签元数据
# - "products"标签：描述"产品管理相关操作"
# - "orders"标签：描述"订单处理和管理"，带外部文档链接
# - "users"标签：描述"用户账户管理"


# 题目3：创建以下路径操作并使用对应标签
# - GET /products：返回产品列表，使用"products"标签
# - GET /orders：返回订单列表，使用"orders"标签
# - GET /users：返回用户列表，使用"users"标签


# 题目4：配置OpenAPI和文档URLs
# - OpenAPI schema路径："/api/openapi.json"
# - Swagger UI路径："/api/docs"
# - ReDoc路径："/api/redoc"


# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
