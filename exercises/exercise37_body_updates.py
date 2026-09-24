# 练习37：请求体更新（Body - Updates）
# 要求：根据注释要求实现相应的FastAPI应用

# 题目1：PUT整体替换
# 创建Item模型: name(str), description(可选str), price(float), tax(float=10.5)
# 创建内存字典items_db预置1条数据
# 创建PUT接口 /items/{item_id}，直接用新数据整体替换旧数据
# 观察未传的tax字段会被默认值10.5覆盖

# 题目2：PATCH局部更新
# 创建ItemUpdate模型，所有字段均为可选（默认None）
# 创建PATCH接口 /items/{item_id}
# 使用 update_data = body.model_dump(exclude_unset=True) 过滤未设置字段

# 题目3：合并更新
# 使用 stored_item_model.model_copy(update=update_data) 生成新对象
# 将合并结果存回items_db，返回更新后的完整数据

# 题目4：对比验证
# 分别用PUT和PATCH只更新price字段
# 在注释中回答：tax字段的值在两种方式下分别是什么，为什么

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
