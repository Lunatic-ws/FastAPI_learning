# 练习39：Security简介
# 要求：根据注释要求实现相应的FastAPI应用
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

SECRET_TOKEN = "secret-token-123"

# 题目1：概念理解（在注释中回答）
# 认证(Authentication)和授权(Authorization)的区别是什么
# 各举一个装修行业SaaS中的实际例子

AUTH_VS_AUTHORIZATION = {
    "authentication": {
        "name": "认证 Authentication",
        "meaning": "确认请求方到底是谁，即让系统知道你的身份",
        "renovation_saas_example": "设计师用手机号加验证码（或企业SSO）登录家装SaaS后台，平台据此识别他属于哪家装企",
        "http_example": "登录接口校验账号密码并签发token，之后的请求都带上这个token",
    },
    "authorization": {
        "name": "授权 Authorization",
        "meaning": "身份确认之后再判断他能访问哪些资源、能执行哪些操作，即你能做什么",
        "renovation_saas_example": "设计师只能查看本门店的量房单与报价单，店长可以查看并修改全部门店数据，老板才能看到利润与结算",
        "http_example": "受保护接口在认证通过后，再按角色和门店范围做数据过滤与操作校验",
    },
    "order": "先认证后授权：认证失败返回401，认证通过但权限不足返回403",
}


@app.get("/security/concepts")
def read_security_concepts() -> dict:
    return AUTH_VS_AUTHORIZATION

# 题目2：手动实现简单Token校验
# 创建POST接口 /items/
# 从请求头读取 x-token: str = Header(...)
# 与预设的合法token（如"secret-token-123"）比对，不匹配则拒绝

TOKEN_AUTH_HEADERS = {"WWW-Authenticate": "Bearer"}


@app.post("/items/")
def create_item_with_manual_token(x_token: str = Header(...)) -> dict:
    if x_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="无效的x-token")
    return {"name": "地板砖", "quantity": 12, "token_validated": True}

# 题目3：返回401未授权
# 校验失败时抛出 HTTPException(status_code=401, detail="无效的token")
# 在 /docs 中观察该接口的响应说明

@app.post("/items/token/")
def create_item_with_401(x_token: str = Header(...)) -> dict:
    if x_token != SECRET_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="无效的token",
            headers=TOKEN_AUTH_HEADERS,
        )
    return {"name": "乳胶漆", "quantity": 3, "token_validated": True}

# 题目4：用依赖复用校验逻辑
# 将token校验封装为依赖函数 verify_token
# 创建2个受保护接口（/items/ 和 /orders/）都使用 Depends(verify_token)
# 在注释中回答：为什么不把校验代码复制到每个接口里

DEPENDENCY_RATIONALE = {
    "question": "为什么不把校验代码复制到每个接口里",
    "answer": "复制校验代码会造成重复劳动且容易漏改，一旦token规则升级就需要逐个接口排查；封装成依赖后校验逻辑只有一份，FastAPI在请求进入接口前统一执行，还能自动生成OpenAPI中的安全声明。新增接口只需写Depends(verify_token)，业务代码与安全代码彻底分离，也更容易单元测试和替换实现。",
}


def verify_token(x_token: str = Header(...)) -> str:
    if x_token != SECRET_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="无效的token",
            headers=TOKEN_AUTH_HEADERS,
        )
    return x_token


@app.get("/items/protected/")
def read_protected_items(token: str = Depends(verify_token)) -> dict:
    return {"items": ["瓷砖", "防水涂料"], "token": token}


@app.get("/orders/")
def read_protected_orders(token: str = Depends(verify_token)) -> dict:
    return {"orders": [{"order_id": 1, "customer": "张先生"}], "token": token}


@app.get("/security/dependency-rationale")
def read_dependency_rationale() -> dict:
    return DEPENDENCY_RATIONALE

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
