# 练习28：额外模型

# 要求：
# 1. 定义三个用户模型：UserIn、UserOut、UserInDB
# 2. UserIn 包含：username, password, email, full_name(可选)
# 3. UserOut 不应包含密码
# 4. UserInDB 应包含 hashed_password 而非 password
# 5. 创建一个基类 UserBase 减少代码重复
# 6. 实现用户创建API：POST /users/
#    - 接收 UserIn
#    - 返回 UserOut
#    - 模拟保存到数据库（UserInDB）
# 7. 实现一个返回多种类型item的API：GET /items/{item_id}
#    - 可以返回 CarItem 或 PlaneItem
#    - 使用 Union 类型

# 题目1：定义模型基类和三个用户模型
# 使用继承，基类包含共享字段

# 题目2：实现密码哈希函数和用户保存函数
# fake_password_hasher(raw_password: str) -> str
# fake_save_user(user_in: UserIn) -> UserInDB

# 题目3：创建用户API
# POST /users/
# 使用 response_model=UserOut

# 题目4：定义物品模型
# BaseItem, CarItem, PlaneItem
# CarItem 和 PlaneItem 继承 BaseItem

# 题目5：实现获取物品API
# GET /items/{item_id}
# 返回 Union[CarItem, PlaneItem]
# 预设一些测试数据

if __name__ == "__main__":
    pass
