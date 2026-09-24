# 练习27: 响应模型
# 要求：根据注释要求实现相应的FastAPI应用

# 题目1: 基础响应模型
# 创建一个POST接口 /items/
# Item模型: name(str), description(可选str), price(float), tags(list[str],默认[])
# 使用返回类型注解声明响应模型
# 返回接收到的item

# 题目2: 列表响应模型
# 创建一个GET接口 /items/
# 返回类型: list[Item]
# Item模型: name(str), price(float)
# 返回包含2个Item的列表

# 题目3: 密码过滤（安全）
# 创建UserIn模型: username(str), password(str), email(str)
# 创建UserOut模型: username(str), email(str)
# 创建一个POST接口 /users/
# 接收UserIn，使用response_model=UserOut返回
# 确保password不会出现在响应中

# 题目4: 模型继承
# 创建BaseUser模型: username(str), email(str), full_name(可选str)
# 创建UserIn模型继承BaseUser，添加password(str)
# 创建一个POST接口 /users/inherit
# 接收UserIn，返回类型注解为BaseUser
# 确保编辑器不报错，且password被过滤

# 题目5: 排除未设置字段
# 创建Product模型: name(str), description(可选str), price(float), tax(float=10.5), tags(list[str]=[])
# 创建一个GET接口 /products/{product_id}
# 使用response_model_exclude_unset=True
# 创建products字典包含至少2个产品（一个只有必需字段，一个有可选字段）
# 观察返回结果的差异

# 题目6: 包含/排除特定字段
# 创建Item模型: name(str), description(可选str), price(float), secret_code(str)
# 创建一个GET接口 /items/{item_id}/public
# 使用response_model_exclude排除secret_code字段
# 创建一个GET接口 /items/{item_id}/brief
# 使用response_model_include只包含name和price字段

# 题目7: response_model与Any
# 创建Item模型: name(str), price(float)
# 创建一个POST接口 /items/any
# 接收Item，使用response_model=Item
# 返回类型注解为Any
# 返回一个字典（非Item对象），验证response_model会自动转换

# 题目8: 嵌套模型响应
# 创建Address模型: street(str), city(str), country(str)
# 创建User模型: name(str), age(int), address(Address)
# 创建一个GET接口 /users/{user_id}
# 返回类型为User
# 返回一个包含嵌套address的用户对象

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
