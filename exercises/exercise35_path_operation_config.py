# 练习35：路径操作配置
# 要求：学习配置路径操作的status_code、tags、summary、description、response_description、deprecated

# 题目1：设置响应状态码
# 创建一个FastAPI应用
# 定义Pydantic模型Product，包含字段：name (str), price (float)
# 创建POST路径 /products/，设置status_code为201 (使用status.HTTP_201_CREATED)
# 返回创建的product
# 测试：POST请求应返回201状态码

# 题目2：使用标签分组
# 创建两个路径：
# 1. GET /books/ - tags=["books"]，返回书籍列表
# 2. GET /authors/ - tags=["authors"]，返回作者列表
# 在自动文档中，这两个路径应该分别显示在"books"和"authors"分组下
# 测试：访问 /docs 查看分组效果

# 题目3：使用枚举管理标签
# 定义枚举类Tags，包含：books = "books", authors = "authors", users = "users"
# 创建三个路径，分别使用Tags枚举作为tags参数：
# 1. GET /books/ - tags=[Tags.books]
# 2. GET /authors/ - tags=[Tags.authors]
# 3. GET /users/ - tags=[Tags.users]
# 测试：确保文档中标签正确显示

# 题目4：添加摘要和描述
# 创建POST路径 /orders/
# 设置summary为"Place a new order"
# 设置description为"Create a new order with customer information and product details. "
# description继续："The order will be processed and a confirmation will be sent."
# 定义Pydantic模型Order，包含：customer_name (str), product_id (int), quantity (int)
# 测试：在自动文档中查看摘要和描述

# 题目5：从文档字符串获取描述
# 创建GET路径 /products/{product_id}
# 设置summary为"Get product details"
# 在函数文档字符串中写详细描述（使用Markdown格式）：
# """
# Retrieve detailed information about a specific product.
# 
# Parameters:
# - **product_id**: The unique identifier of the product
# 
# Returns:
# - Product name, description, and price
# """
# 测试：在自动文档中查看格式化的描述

# 题目6：设置响应描述
# 创建POST路径 /customers/
# 设置summary为"Register new customer"
# 设置response_description为"Customer successfully registered with assigned ID"
# 定义Pydantic模型Customer，包含：name (str), email (str)
# 测试：在自动文档的响应部分查看响应描述

# 题目7：标记为已弃用
# 创建三个路径：
# 1. GET /api/v1/items/ - 正常路径
# 2. GET /api/v1/users/ - 正常路径
# 3. GET /api/v1/old-endpoint/ - 设置deprecated=True
# 测试：在自动文档中，第三个路径应显示为已弃用（带删除线）

# 题目8：综合配置
# 定义Pydantic模型Article，包含：title (str), content (str), author (str)
# 创建POST路径 /articles/，配置：
# - status_code: 201
# - tags: ["articles"]
# - summary: "Publish a new article"
# - description写在文档字符串中（包含Markdown格式的字段说明）
# - response_description: "Article published successfully with article ID"
# 测试：在自动文档中验证所有配置都正确显示

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
