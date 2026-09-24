# 练习43：带JWT的OAuth2（OAuth2 with Password and JWT）
# 要求：根据注释要求实现相应的FastAPI应用
# 说明：需要 pip install pyjwt "passlib[bcrypt]"

# 题目1：密码哈希
# 创建 pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 实现 verify_password(plain, hashed) 和 get_password_hash(password)

# 题目2：模拟用户数据库
# 创建fake_users_db，用户字段包含 hashed_password（用get_password_hash生成）
# 其他字段: username, full_name, email, disabled(bool)

# 题目3：JWT的创建与配置
# 定义 SECRET_KEY、ALGORITHM="HS256"、ACCESS_TOKEN_EXPIRE_MINUTES=30
# 实现 create_access_token(data: dict)：
# 在data中拷贝加入 "exp"（过期时间，使用datetime.now(timezone.utc) + timedelta）
# 使用 jwt.encode 生成token

# 题目4：登录端点
# 创建POST接口 /token/，校验用户存在、密码verify通过、用户未disabled
# 失败时抛出 HTTPException(401, detail="错误的用户名或密码")
# 成功时返回 create_access_token 生成的JWT

# 题目5：解码JWT获取当前用户
# 实现 get_current_user 依赖：jwt.decode 解码token
# 处理 jwt.ExpiredSignatureError（返回401"token已过期"）
# 处理解码失败和用户不存在（返回401"无效的凭据"）
# 实现 get_current_active_user：disabled用户返回400
# 创建 /users/me/ 受保护接口，用 /docs 的Authorize完整测试

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
