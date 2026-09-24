# 练习39：Security简介
# 要求：根据注释要求实现相应的FastAPI应用

# 题目1：概念理解（在注释中回答）
# 认证(Authentication)和授权(Authorization)的区别是什么
# 各举一个装修行业SaaS中的实际例子

# 题目2：手动实现简单Token校验
# 创建POST接口 /items/
# 从请求头读取 x-token: str = Header(...)
# 与预设的合法token（如"secret-token-123"）比对，不匹配则拒绝

# 题目3：返回401未授权
# 校验失败时抛出 HTTPException(status_code=401, detail="无效的token")
# 在 /docs 中观察该接口的响应说明

# 题目4：用依赖复用校验逻辑
# 将token校验封装为依赖函数 verify_token
# 创建2个受保护接口（/items/ 和 /orders/）都使用 Depends(verify_token)
# 在注释中回答：为什么不把校验代码复制到每个接口里

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
