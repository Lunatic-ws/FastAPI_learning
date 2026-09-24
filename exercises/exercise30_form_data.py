# 练习30：表单数据处理
# 要求：创建接收表单数据的接口
# 题目：
# 1. 创建一个POST接口 /login，接收username和password表单字段
#    - username: 最少3个字符
#    - password: 最少6个字符
#    - 返回包含username和登录状态的JSON响应
#
# 2. 创建一个POST接口 /register，接收注册表单数据
#    - username: 必填，最少3个字符
#    - email: 必填
#    - password: 必填，最少6个字符
#    - age: 可选，整数类型
#    - 验证两次密码是否一致
#    - 返回注册成功的用户信息
#
# 3. 创建一个POST接口 /update-profile，支持部分字段更新
#    - name: 必填
#    - nickname: 可选
#    - bio: 可选，默认为空字符串
#    - 返回更新后的用户信息
#
# 提示：
# - 使用 Form() 声明表单参数
# - 使用 Form(min_length=3) 添加验证
# - 使用 Optional[str] 和 Form(default=None) 声明可选字段
#
# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
